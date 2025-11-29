# config.py
import os
from pathlib import Path

ROOT = Path(__file__).parent

# Paths
MEDIA_DIR = str(ROOT / "media")
VIDEO_DIR = str(ROOT / "media" / "videos")
THUMB_DIR = str(ROOT / "media" / "thumbs")
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(THUMB_DIR, exist_ok=True)

# YouTube / OAuth files (placed during setup)
CLIENT_SECRETS_FILE = str(ROOT / "client_secret.json")
TOKEN_FILE = str(ROOT / "token.json")

# Optional: set your OpenAI API key in GitHub Secrets or environment if you want better quotes
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# YouTube defaults
YOUTUBE_CATEGORY = "22"   # People & Blogs
IS_MADE_FOR_KIDS = False

# Video defaults
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
DURATION_SECONDS = 8

# Operational
BATCH_SLEEP_SECONDS = 15   # wait between uploads in a batch to reduce quota spikes
