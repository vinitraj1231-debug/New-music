from pyrogram import filters
from bot.core.client import bot
from bot.services.playlist_service import playlist_service

@bot.on_message(filters.command("playlist") & filters.group)
async def playlist_command(_, message):
    user_id = message.from_user.id
    playlists = await playlist_service.get_user_playlists(user_id)
    if not playlists:
        return await message.reply("You have no playlists.")

    text = "**Your Playlists:**\n\n"
    for p in playlists:
        text += f"- {p['name']} ({len(p['songs'])} songs)\n"
    await message.reply(text)
