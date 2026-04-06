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
    def __init__(self) -> None:
        self.secret_key = _required_env("SECRET_KEY")
        self.debug = _env_bool("DEBUG", False)

        self.ridwaanhall_main_api = _env("RIDWAANHALL_MAIN_API", "https://internal.invalid")
        self.api_key = _required_env("API_KEY")

        self.ridwaanhall_api_x = _env("RIDWAANHALL_API_X", "X-Private-Api-Host")
        self.ridwaanhall_x = _env("RIDWAANHALL_X", "X-Private-Origin")
        self.ridwaanhall_hash_x = _env("RIDWAANHALL_HASH_X", "X-Private-Referer")

        self.ridwaanhall_api_key = _env("RIDWAANHALL_API_KEY", "private-api-key")
        self.ridwaanhall_key = _env("RIDWAANHALL_KEY", "private-origin")
        self.ridwaanhall_hash_key = _env("RIDWAANHALL_HASH_KEY", "private-referer")

        self.api_availability = _env_bool("API_AVAILABILITY", True)
        self.api_version = _env("API_VERSION", "4.0.0")
        self.last_update = _env("LAST_UPDATE", "2026-05-29T00:00:00+07:00")
        self.api_timeout = _env_int("API_TIMEOUT", 8)
        self.public_base_url = _env("PUBLIC_BASE_URL", "https://pddikti.rone.dev").rstrip("/")


@lru_cache
def get_settings() -> Settings:
    return Settings()
