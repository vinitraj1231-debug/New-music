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
        self.supreme_users = self.db["supreme_users"]
        self.served_users = self.db["served_users"]
        self.served_groups = self.db["served_groups"]

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

    # Clone management
    async def add_clone(self, bot_token, api_id, api_hash, string_session, user_id):
        return await self.clone_profiles.update_one(
            {"bot_token": bot_token},
            {
                "$set": {
                    "api_id": api_id,
                    "api_hash": api_hash,
                    "string_session": string_session,
                    "user_id": user_id,
                }
            },
            upsert=True
        )

    async def remove_clone(self, bot_token):
        return await self.clone_profiles.delete_one({"bot_token": bot_token})

    async def get_clones(self):
        return await self.clone_profiles.find().to_list(length=None)

    # Supreme users management
    async def is_supreme(self, user_id):
        if user_id == config.OWNER_ID:
            return True
        user = await self.supreme_users.find_one({"user_id": user_id})
        return True if user else False

    async def add_supreme(self, user_id):
        return await self.supreme_users.update_one(
            {"user_id": user_id},
            {"$set": {"user_id": user_id}},
            upsert=True
        )

    async def remove_supreme(self, user_id):
        return await self.supreme_users.delete_one({"user_id": user_id})

    async def get_supreme_users(self):
        return await self.supreme_users.find().to_list(length=None)

    # Broadcast helpers
    async def add_served_user(self, user_id):
        return await self.served_users.update_one(
            {"user_id": user_id},
            {"$set": {"user_id": user_id}},
            upsert=True
        )

    async def add_served_group(self, chat_id):
        return await self.served_groups.update_one(
            {"chat_id": chat_id},
            {"$set": {"chat_id": chat_id}},
            upsert=True
        )

    async def get_served_users(self):
        return await self.served_users.find().to_list(length=None)

    async def get_served_groups(self):
        return await self.served_groups.find().to_list(length=None)

db = Database()
