from pyrogram import filters
from bot.core.client import bot
from bot.services.lyrics_service import lyrics_service

@bot.on_message(filters.command("lyrics"))
async def lyrics_command(_, message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Provide a song name.")

    lyrics = await lyrics_service.get_lyrics(query)
    await message.reply(lyrics)
