from pyrogram import filters, Client
from bot.services.lyrics_service import lyrics_service

@Client.on_message(filters.command("lyrics"))
async def lyrics_command(client, message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("Provide a song name.")

    lyrics = await lyrics_service.get_lyrics(query)
    await message.reply(lyrics)
