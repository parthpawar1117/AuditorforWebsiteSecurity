import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
# Hosted deployments set CYBERSENTINEL_DB_PATH (e.g. /tmp/cybersentinel.db) because
# their filesystem is read-only; locally the database stays next to the project.
DB_PATH = Path(os.getenv("CYBERSENTINEL_DB_PATH", str(BASE_DIR / "cybersentinel.db")))

# Hosted public demo: only the built-in /mock test bench may be scanned.
DEMO_MODE = os.getenv("CYBERSENTINEL_DEMO_MODE") == "1"

PROJECT_NAME = "CyberSentinel"
VERSION = "1.0.0"
STUDENT_NAME = "Parth Pawar & Aryaman V Saboo"
STUDENT_ROLL = "2024SEPVUGP0021 & 2024SEPVUGP0039"
COURSE_NAME = "Foundation of Cyber Security (STCS225)"
UNIVERSITY = "Vijaybhoomi University - VSST"

SCAN_TIMEOUT = 12.0  # seconds
USER_AGENT = "CyberSentinel-SecurityAuditor/1.0 (Ethical Defensive Assessment; Parth-Pawar-2024SEPVUGP0021-Aryaman-Saboo-2024SEPVUGP0039)"

# Safe mock testing server ports/paths
MOCK_SERVER_HOST = "127.0.0.1"
MOCK_SERVER_PORT = 8000
