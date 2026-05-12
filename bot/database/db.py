from motor.motor_asyncio import AsyncIOMotorClient
from bot.config.config import config

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(config.MONGO_DB_URI)
        self.db = self.client["music_bot"]

        # Collections
        self.users = self.db["users"]
        self.groups = self.db["groups"]
        self.queues = self.db["queues"]
        self.playlists = self.db["playlists"]
        self.settings = self.db["settings"]
        self.authusers = self.db["authusers"]
        self.filters = self.db["filters"]
        self.clone_profiles = self.db["clone_profiles"]
        self.logs = self.db["logs"]
        self.stats = self.db["stats"]

    async def get_group_settings(self, chat_id):
        settings = await self.settings.find_one({"chat_id": chat_id})
        if not settings:
            settings = {
                "chat_id": chat_id,
                "dj_mode": False,
                "admin_only": False,
                "cooldown": 5,
                "theme": "dark",
                "quality": "high"
            }
            await self.settings.insert_one(settings)
        return settings

db = Database()
