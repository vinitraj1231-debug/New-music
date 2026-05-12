import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    STRING_SESSION = os.getenv("STRING_SESSION", "")
    MONGO_DB_URI = os.getenv("MONGO_DB_URI", "")
    OWNER_ID = int(os.getenv("OWNER_ID", "0"))
    LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "0"))
    SUDO_USERS = list(map(int, os.getenv("SUDO_USERS", "").split())) if os.getenv("SUDO_USERS") else []

    # Defaults
    DURATION_LIMIT = int(os.getenv("DURATION_LIMIT", "3600")) # 1 hour
    CACHE_DIR = "bot/cache"
    SESSION_DIR = "bot/sessions"

config = Config()
