from pyrogram import Client
from bot.config.config import config

bot = Client(
    "MusicBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="bot.plugins"),
    sleep_threshold=60,
    max_concurrent_transmissions=3
)

assistant = Client(
    "Assistant",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.STRING_SESSION,
    sleep_threshold=60,
    max_concurrent_transmissions=3
)
