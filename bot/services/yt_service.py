import asyncio
import yt_dlp
from bot.config.config import config

class YTService:
    def __init__(self):
        self.ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{config.CACHE_DIR}/%(id)s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
        }

    async def search(self, query):
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                info = await loop.run_in_executor(
                    None, lambda: ydl.extract_info(f"ytsearch:{query}", download=False)
                )
                if not info["entries"]:
                    return None
                return info["entries"][0]
            except Exception as e:
                print(f"YT Search Error: {e}")
                return None

    async def extract_info(self, url):
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                info = await loop.run_in_executor(
                    None, lambda: ydl.extract_info(url, download=False)
                )
                return info
            except Exception as e:
                print(f"YT Extract Error: {e}")
                return None

    async def download(self, url):
        loop = asyncio.get_event_loop()
        # We might need separate opts for download to ensure we get specific audio format or path
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                info = await loop.run_in_executor(
                    None, lambda: ydl.extract_info(url, download=True)
                )
                return ydl.prepare_filename(info)
            except Exception as e:
                print(f"YT Download Error: {e}")
                return None

yt_service = YTService()
