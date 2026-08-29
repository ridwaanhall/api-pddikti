from functools import lru_cache
import os

from dotenv import load_dotenv


load_dotenv()


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            "Set it in deployment environment variables or local .env file."
        )
    return value


def _env(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return value


def _parse_bool(name: str, value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise RuntimeError(
        f"Invalid boolean value for {name}: {value!r}. Use true/false, 1/0, yes/no, or on/off."
    )


def _required_bool(name: str) -> bool:
    return _parse_bool(name, _required_env(name))


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return _parse_bool(name, value)


def _required_int(name: str) -> int:
    value = _required_env(name)
    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(f"Invalid integer value for {name}: {value!r}") from exc


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(f"Invalid integer value for {name}: {value!r}") from exc


class Settings:
    """Runtime configuration.

    No upstream, deployment, or third-party host is hardcoded here. Every URL comes from
    the environment, so this source tree can be published without disclosing which hosts
    the service talks to. Anything left unset simply disables the feature that needs it
    rather than failing at import time -- see the `upstream` block on `GET /api/` to
    confirm what a running deployment actually resolved.
    """

    def __init__(self) -> None:
        # ---------------------------------------------------------------- branding
        self.brand_name = _env("BRAND_NAME", "Sivitas API")
        self.brand_owner = _env("BRAND_OWNER", "RoneAI")
        self.maintainer = _env("MAINTAINER", "ridwaanhall")
        self.brand_tagline = _env(
            "BRAND_TAGLINE", "Structured access to Indonesian higher-education data."
        )
        # Named for attribution and for the non-affiliation notice below. Both of those
        # only mean something if the source can be named, so this is not a secret.
        self.data_source_name = _env("DATA_SOURCE_NAME", "PDDikti")

        self.required_credit_line = _env(
            "CREDIT_LINE",
            f"Powered by {self.brand_name}, data sourced from {self.data_source_name}, "
            f"maintained by {self.maintainer} / {self.brand_owner}",
        )
        self.disclaimer = _env(
            "DISCLAIMER",
            f"{self.brand_name} is an independent, community-maintained project. It is "
            f"not affiliated with, endorsed by, sponsored by, or operated by "
            f"{self.data_source_name} or any government body. It reads publicly "
            f"available higher-education data and re-serves it in a structured form; the "
            f"underlying data belongs to its original publisher and all rights remain "
            f"with them. Data is provided as-is, with no warranty of accuracy, "
            f"completeness, or availability -- verify anything consequential against the "
            f"official source before relying on it.",
        )

        # ------------------------------------------------------------------- secrets
        self.secret_key = _env("SECRET_KEY", "")
        self.api_key = _env("API_KEY", "")
        self.debug = _env_bool("DEBUG", False)

        # ------------------------------------------------- primary upstream (env only)
        self.upstream_origin = _env("UPSTREAM_ORIGIN", "").rstrip("/")
        self.upstream_base_url = _env("UPSTREAM_BASE_URL", "").rstrip("/")
        self.upstream_decrypt_url = _env("UPSTREAM_DECRYPT_URL", "")

        # Browser TLS/JA3 impersonation profile, used when curl_cffi is installed.
        # Plain header spoofing is not enough for edges that fingerprint the TLS
        # handshake itself; this is what gets a datacenter IP past that check.
        # A blank value means "use the default" like every other setting here, so
        # disabling needs an explicit opt-out keyword.
        impersonate = _env("UPSTREAM_IMPERSONATE", "chrome")
        if impersonate.strip().lower() in {"none", "off", "false", "disabled", "0"}:
            impersonate = ""
        self.upstream_impersonate = impersonate

        # Optional cookie header replayed on every upstream call. Escape hatch for an
        # edge that demands a clearance cookie; note such cookies are usually bound to
        # the IP and User-Agent that obtained them.
        self.upstream_cookie = _env("UPSTREAM_COOKIE", "")

        # ------------------------------------------ optional authenticated fallback
        self.ridwaanhall_main_api = _env("RIDWAANHALL_MAIN_API", "").rstrip("/")
        self.ridwaanhall_api_x = _env("RIDWAANHALL_API_X", "")
        self.ridwaanhall_x = _env("RIDWAANHALL_X", "")
        self.ridwaanhall_hash_x = _env("RIDWAANHALL_HASH_X", "")
        self.ridwaanhall_api_key = _env("RIDWAANHALL_API_KEY", "")
        self.ridwaanhall_key = _env("RIDWAANHALL_KEY", "")
        self.ridwaanhall_hash_key = _env("RIDWAANHALL_HASH_KEY", "")

        # ----------------------------------------------------------- caller IP lookup
        # Used only when the caller's own IP is not routable. Unset disables the lookup.
        self.ip_lookup_url = _env("IP_LOOKUP_URL", "")
        self.ip_cache_ttl = _env_int("IP_CACHE_TTL", 3600)

        # -------------------------------------------------------------- this service
        self.api_availability = _env_bool("API_AVAILABILITY", True)
        self.api_version = _env("API_VERSION", "5.0.0")
        self.last_update = _env("LAST_UPDATE", "2026-08-29T00:00:00+07:00")
        self.api_timeout = _env_int("API_TIMEOUT", 10)
        # The decrypt leg uploads and downloads far more than a normal call, so it
        # gets its own budget instead of silently blowing the standard timeout.
        self.decrypt_timeout = _env_int("DECRYPT_TIMEOUT", max(self.api_timeout, 20))
        self.public_base_url = _env("PUBLIC_BASE_URL", "").rstrip("/")

        # Optional second deployment advertised when this one is rate-limited.
        self.alternative_base_url = _env("ALTERNATIVE_BASE_URL", "").rstrip("/")
        self.alternative_name = _env("ALTERNATIVE_NAME", "High Availability Endpoint")

        # --------------------------------------------------------- support + web chrome
        self.support_email = _env("SUPPORT_EMAIL", "")
        self.support_chat_url = _env("SUPPORT_CHAT_URL", "")
        self.support_contact_url = _env("SUPPORT_CONTACT_URL", "")
        self.website_url = _env("WEBSITE_URL", "")
        self.favicon_url = _env("FAVICON_URL", "")
        self.analytics_id = _env("ANALYTICS_ID", "")

    @property
    def support_links(self) -> dict[str, str]:
        """Only the support channels that are actually configured."""
        links = {
            "live_chat": self.support_chat_url,
            "email": self.support_email,
            "contact_form": self.support_contact_url,
        }
        return {key: value for key, value in links.items() if value}

    @property
    def alternative_endpoints(self) -> list[dict[str, str]]:
        if not self.alternative_base_url:
            return []
        return [
            {
                "name": self.alternative_name,
                "url": self.alternative_base_url,
                "description": (
                    "Alternative endpoint designed to remain available during high "
                    "traffic periods."
                ),
            }
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
