from pyrogram import filters, Client
from bot.services.playlist_service import playlist_service

@Client.on_message(filters.command("playlist") & filters.group)
async def playlist_command(client, message):
    user_id = message.from_user.id
    playlists = await playlist_service.get_user_playlists(user_id)
    if not playlists:
        return await message.reply("You have no playlists.")

    text = "**Your Playlists:**\n\n"
    for p in playlists:
        text += f"- {p['name']} ({len(p['songs'])} songs)\n"
    await message.reply(text)
