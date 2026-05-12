import asyncio
from pytgcalls.types import MediaStream
from bot.core.call import call_py
from bot.services.queue_service import queue_service
from bot.services.yt_service import yt_service

class PlaybackService:
    def __init__(self):
        self.active_calls = set()

    async def play(self, chat_id, song_data):
        url = song_data["link"]
        # In a real production bot, we might want to pre-download or stream directly
        # For simplicity and following requirements, we use yt-dlp to get stream link or file

        # Simple extraction of direct stream URL using yt-dlp if it's a YouTube link
        info = await yt_service.extract_info(url)
        if not info:
            return False

        stream_url = None
        for fmt in info.get("formats", []):
            if fmt.get("acodec") != "none" and fmt.get("vcodec") == "none":
                stream_url = fmt.get("url")
                break

        if not stream_url:
            stream_url = info.get("url")

        try:
            await call_py.play(
                chat_id,
                MediaStream(stream_url)
            )
            self.active_calls.add(chat_id)
            return True
        except Exception as e:
            print(f"Playback Error: {e}")
            return False

    async def skip(self, chat_id):
        await queue_service.pop_from_queue(chat_id)
        next_song = await queue_service.get_queue(chat_id)
        if next_song:
            return await self.play(chat_id, next_song[0])
        else:
            await self.stop(chat_id)
            return None

    async def stop(self, chat_id):
        try:
            await call_py.leave_call(chat_id)
        except Exception:
            pass
        if chat_id in self.active_calls:
            self.active_calls.remove(chat_id)
        await queue_service.clear_queue(chat_id)

playback_service = PlaybackService()
