from bot.database.db import db

class PlaylistService:
    async def create_playlist(self, user_id, name):
        await db.playlists.insert_one({"user_id": user_id, "name": name, "songs": []})

    async def add_to_playlist(self, user_id, name, song_data):
        await db.playlists.update_one(
            {"user_id": user_id, "name": name},
            {"$push": {"songs": song_data}}
        )

    async def get_user_playlists(self, user_id):
        return await db.playlists.find({"user_id": user_id}).to_list(length=100)

playlist_service = PlaylistService()
