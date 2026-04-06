from pathlib import Path
import os
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# Required env vars for strict settings (no defaults).
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("RIDWAANHALL_MAIN_API", "https://api-pddikti.kemdiktisaintek.go.id")
os.environ.setdefault("API_KEY", "test-api-key")
os.environ.setdefault("RIDWAANHALL_API_X", "Host")
os.environ.setdefault("RIDWAANHALL_X", "Origin")
os.environ.setdefault("RIDWAANHALL_HASH_X", "Referer")
os.environ.setdefault("RIDWAANHALL_API_KEY", "api-pddikti.kemdiktisaintek.go.id")
os.environ.setdefault("RIDWAANHALL_KEY", "https://pddikti.kemdiktisaintek.go.id")
os.environ.setdefault("RIDWAANHALL_HASH_KEY", "https://pddikti.kemdiktisaintek.go.id/")
os.environ.setdefault("API_AVAILABILITY", "true")
os.environ.setdefault("API_VERSION", "4.0.0")
os.environ.setdefault("LAST_UPDATE", "2026-05-29T00:00:00+07:00")
os.environ.setdefault("API_TIMEOUT", "8")
