from pyrogram import filters, Client
from bot.config.config import config
from bot.database.db import db

async def is_admin(client, chat_id, user_id):
    if user_id == config.OWNER_ID or user_id in config.SUDO_USERS:
        return True
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except Exception:
        return False

@Client.on_message(filters.command("settings") & filters.group)
async def settings_command(client, message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply("Only admins can change settings.")

    settings = await db.get_group_settings(message.chat.id)
    text = f"**Settings for {message.chat.title}**\n\n"
    text += f"DJ Mode: {'Enabled' if settings['dj_mode'] else 'Disabled'}\n"
    text += f"Admin Only: {'Enabled' if settings['admin_only'] else 'Disabled'}\n"

    await message.reply(text)

@Client.on_message(filters.command("addsudo") & filters.user(config.OWNER_ID))
async def add_sudo(client, message):
    if not message.reply_to_message:
        return await message.reply("Reply to a user to add them as sudo.")
    user_id = message.reply_to_message.from_user.id
    if user_id not in config.SUDO_USERS:
        config.SUDO_USERS.append(user_id)
        # Update in DB or env as well in a real app
        await message.reply(f"User {user_id} added to Sudo Users.")
    else:
        await message.reply("User is already a Sudo User.")
