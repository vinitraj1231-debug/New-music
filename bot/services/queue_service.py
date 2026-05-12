from bot.database.db import db

class QueueService:
    def __init__(self):
        self.queues = {} # In-memory cache for fast access, synced with MongoDB

    async def add_to_queue(self, chat_id, song_data):
        if chat_id not in self.queues:
            self.queues[chat_id] = []
        self.queues[chat_id].append(song_data)
        # Persistence
        await db.queues.update_one(
            {"chat_id": chat_id},
            {"$push": {"queue": song_data}},
            upsert=True
        )

    async def get_queue(self, chat_id):
        if chat_id in self.queues:
            return self.queues[chat_id]

        doc = await db.queues.find_one({"chat_id": chat_id})
        if doc:
            self.queues[chat_id] = doc.get("queue", [])
            return self.queues[chat_id]
        return []

    async def pop_from_queue(self, chat_id):
        queue = await self.get_queue(chat_id)
        if not queue:
            return None
        song = queue.pop(0)
        await db.queues.update_one(
            {"chat_id": chat_id},
            {"$set": {"queue": queue}}
        )
        return song

    async def clear_queue(self, chat_id):
        self.queues[chat_id] = []
        await db.queues.delete_one({"chat_id": chat_id})

    async def shuffle_queue(self, chat_id):
        import random
        queue = await self.get_queue(chat_id)
        if len(queue) > 1:
            first_song = queue.pop(0)
            random.shuffle(queue)
            queue.insert(0, first_song)
            self.queues[chat_id] = queue
            await db.queues.update_one(
                {"chat_id": chat_id},
                {"$set": {"queue": queue}}
            )

queue_service = QueueService()
