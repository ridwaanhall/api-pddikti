from pathlib import Path
import os
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# Runtime env vars for predictable test configuration.
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("DEBUG", "false")
os.environ.setdefault("PUBLIC_BASE_URL", "https://api.example.test")
os.environ.setdefault("API_KEY", "test-api-key")
os.environ.setdefault("API_AVAILABILITY", "true")
os.environ.setdefault("API_VERSION", "4.0.0")
os.environ.setdefault("LAST_UPDATE", "2026-05-29T00:00:00+07:00")
os.environ.setdefault("API_TIMEOUT", "8")

# Upstream hosts are env-only in this project -- nothing is hardcoded in the source,
# so tests must supply their own. These are unreachable placeholders; every test that
# exercises the client stubs the HTTP layer.
os.environ.setdefault("UPSTREAM_ORIGIN", "https://upstream.example.test")
os.environ.setdefault("UPSTREAM_BASE_URL", "https://upstream.example.test/api")
os.environ.setdefault("UPSTREAM_DECRYPT_URL", "https://upstream.example.test/internal/decrypt")
os.environ.setdefault("IP_LOOKUP_URL", "https://ip.example.test/?format=json")
os.environ.setdefault("ALTERNATIVE_BASE_URL", "https://alt.example.test")
os.environ.setdefault("SUPPORT_EMAIL", "support@example.test")

