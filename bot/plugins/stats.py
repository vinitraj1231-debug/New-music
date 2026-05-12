import time
from pyrogram import filters, enums
from bot.core.client import bot
from bot.database.db import db
from datetime import datetime

@bot.on_message(group=1)
async def track_chats(_, message):
    if message.chat.type == enums.ChatType.PRIVATE:
        await db.add_served_user(message.chat.id)
    else:
        await db.add_served_group(message.chat.id)

@bot.on_message(filters.command("ping"))
async def ping_handler(_, message):
    start = time.time()
    m = await message.reply("Pinging...")
    end = time.time()
    latency = (end - start) * 1000
    await m.edit(f"🏓 Pong!\nLatency: {latency:.2f} ms")

@bot.on_message(filters.command("stats"))
async def stats_handler(_, message):
    # In a real app, fetch more stats from DB
    await message.reply(f"Bot Stats:\n- Groups: Not tracked\n- Users: Not tracked")
