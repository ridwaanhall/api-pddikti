from pathlib import Path
import os
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# Runtime env vars for predictable test configuration.
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("DEBUG", "false")
os.environ.setdefault("PUBLIC_BASE_URL", "https://pddikti.rone.dev")
os.environ.setdefault("API_KEY", "test-api-key")
os.environ.setdefault("API_VERSION", "4.0.0")
os.environ.setdefault("LAST_UPDATE", "2026-05-29T00:00:00+07:00")
os.environ.setdefault("API_TIMEOUT", "8")
