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


def _required_bool(name: str) -> bool:
    value = _required_env(name).strip().lower()
    if value in {"1", "true", "yes", "on"}:
        return True
    if value in {"0", "false", "no", "off"}:
        return False
    raise RuntimeError(
        f"Invalid boolean value for {name}: {value!r}. Use true/false, 1/0, yes/no, or on/off."
    )


def _required_int(name: str) -> int:
    value = _required_env(name)
    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(f"Invalid integer value for {name}: {value!r}") from exc


class Settings:
    def __init__(self) -> None:
        self.secret_key = _required_env("SECRET_KEY")
        self.debug = _required_bool("DEBUG")

        self.ridwaanhall_main_api = _required_env("RIDWAANHALL_MAIN_API")
        self.api_key = _required_env("API_KEY")

        self.ridwaanhall_api_x = _required_env("RIDWAANHALL_API_X")
        self.ridwaanhall_x = _required_env("RIDWAANHALL_X")
        self.ridwaanhall_hash_x = _required_env("RIDWAANHALL_HASH_X")

        self.ridwaanhall_api_key = _required_env("RIDWAANHALL_API_KEY")
        self.ridwaanhall_key = _required_env("RIDWAANHALL_KEY")
        self.ridwaanhall_hash_key = _required_env("RIDWAANHALL_HASH_KEY")

        self.api_availability = _required_bool("API_AVAILABILITY")
        self.api_version = _required_env("API_VERSION")
        self.last_update = _required_env("LAST_UPDATE")
        self.api_timeout = _required_int("API_TIMEOUT")


@lru_cache
def get_settings() -> Settings:
    return Settings()
