import time
from pyrogram import filters, enums, Client
from bot.database.db import db
from datetime import datetime

@Client.on_message(group=1)
async def track_chats(client, message):
    if message.chat.type == enums.ChatType.PRIVATE:
        await db.add_served_user(message.chat.id)
    else:
        await db.add_served_group(message.chat.id)

@Client.on_message(filters.command("ping"))
async def ping_handler(client, message):
    start = time.time()
    m = await message.reply("Pinging...")
    end = time.time()
    latency = (end - start) * 1000
    await m.edit(f"🏓 Pong!\nLatency: {latency:.2f} ms")

@Client.on_message(filters.command("stats"))
async def stats_handler(client, message):
    # In a real app, fetch more stats from DB
    await message.reply(f"Bot Stats:\n- Groups: Not tracked\n- Users: Not tracked")
