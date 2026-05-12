from pyrogram import filters
from bot.core.client import bot
from bot.services.yt_service import yt_service
from bot.services.queue_service import queue_service
from bot.services.playback_service import playback_service
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

@bot.on_message(filters.command("play") & filters.group)
async def play_command(_, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Please provide a song name or link.")

    m = await message.reply("🔎 Searching...")
    song = await yt_service.search(query)
    if not song:
        return await m.edit("No results found.")

    song_data = {
        "title": song["title"],
        "link": song["webpage_url"],
        "duration": song.get("duration"),
        "thumbnail": song.get("thumbnail"),
        "requester": message.from_user.mention if message.from_user else "Unknown"
    }

    queue = await queue_service.get_queue(message.chat.id)
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⏸ Pause", callback_data="pause"),
            InlineKeyboardButton("▶️ Resume", callback_data="resume")
        ],
        [
            InlineKeyboardButton("⏭ Skip", callback_data="skip"),
            InlineKeyboardButton("⏹ Stop", callback_data="stop")
        ]
    ])

    if not queue:
        await queue_service.add_to_queue(message.chat.id, song_data)
        success = await playback_service.play(message.chat.id, song_data)
        if success:
            await m.edit(
                f"🎶 **Now Playing**\n\n**Title:** {song_data['title']}\n**Requested by:** {song_data['requester']}",
                reply_markup=buttons
            )
        else:
            await m.edit("Failed to play. Make sure the assistant is in the VC.")
    else:
        await queue_service.add_to_queue(message.chat.id, song_data)
        await m.edit(
            f"📝 **Added to Queue**\n\n**Title:** {song_data['title']}\n**Position:** {len(queue)}",
            reply_markup=buttons
        )

@bot.on_message(filters.command("skip") & filters.group)
async def skip_command(_, message: Message):
    # Admin check would go here
    res = await playback_service.skip(message.chat.id)
    if res is True:
        await message.reply("⏭ Skipped! Playing next song.")
    elif res is None:
        await message.reply("⏭ Skipped! Queue is empty. Leaving VC.")
    else:
        await message.reply("Failed to skip.")

@bot.on_message(filters.command("stop") & filters.group)
async def stop_command(_, message: Message):
    await playback_service.stop(message.chat.id)
    await message.reply("⏹ Stopped and queue cleared.")

@bot.on_message(filters.command("pause") & filters.group)
async def pause_command(_, message: Message):
    from bot.core.call import call_py
    try:
        await call_py.pause(message.chat.id)
        await message.reply("⏸ Paused.")
    except Exception:
        await message.reply("Nothing is playing.")

@bot.on_message(filters.command("resume") & filters.group)
async def resume_command(_, message: Message):
    from bot.core.call import call_py
    try:
        await call_py.resume(message.chat.id)
        await message.reply("▶️ Resumed.")
    except Exception:
        await message.reply("Nothing is paused.")
