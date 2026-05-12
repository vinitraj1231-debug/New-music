import logging
from bot.database.db import db
from datetime import datetime

class Logger:
    def __init__(self):
        self.logger = logging.getLogger("MusicBot")

    async def log_action(self, chat_id, action):
        self.logger.info(f"Chat {chat_id}: {action}")
        await db.logs.insert_one({
            "chat_id": chat_id,
            "action": action,
            "timestamp": datetime.utcnow()
        })

logger_service = Logger()
