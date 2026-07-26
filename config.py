from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
ASSET_DIR = BASE_DIR / "assets"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'mil_database.db'}")
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-development-secret")
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "5"))

ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
UPLOAD_SUBDIRS = {
    "team": UPLOAD_DIR / "team",
    "activities": UPLOAD_DIR / "activities",
    "reality_wall": UPLOAD_DIR / "reality_wall",
    "social_media": UPLOAD_DIR / "social_media",
    "submissions": UPLOAD_DIR / "submissions",
    "resources": UPLOAD_DIR / "resources",
    "website": UPLOAD_DIR / "website",
}

for path in [DATA_DIR, UPLOAD_DIR, ASSET_DIR, *UPLOAD_SUBDIRS.values()]:
    path.mkdir(parents=True, exist_ok=True)
