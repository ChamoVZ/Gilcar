import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "GILCAR_ADMIN")
DB_PASSWORD = os.getenv("DB_PASSWORD", "proyecto2026")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "1521"))
DB_SERVICE = os.getenv("DB_SERVICE", "XEPDB1")
