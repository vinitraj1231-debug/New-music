import asyncio
from pyrogram import filters, types, Client
from bot.database.db import db
from bot.config.config import config

@Client.on_message(filters.command("supreme") & filters.private)
async def supreme_panel(client, message):
    if not await db.is_supreme(message.from_user.id):
        return await message.reply("You don't have Supreme access.")

    buttons = [
        [
            types.InlineKeyboardButton("Manage Clones", callback_data="manage_clones"),
            types.InlineKeyboardButton("Broadcast", callback_data="broadcast_menu"),
        ],
        [
            types.InlineKeyboardButton("Supreme Users", callback_data="manage_supreme"),
        ],
        [
            types.InlineKeyboardButton("Close", callback_data="close_panel"),
        ]
    ]
    await message.reply("Welcome to the **Supreme Panel**.", reply_markup=types.InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex("^manage_clones$"))
async def manage_clones_cb(client, query):
    if not await db.is_supreme(query.from_user.id):
        return await query.answer("Access Denied", show_alert=True)

    clones = await db.get_clones()
    if not clones:
        return await query.edit_message_text("No clones found.", reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton("Back", callback_data="back_to_supreme")]]))

    buttons = []
    for clone in clones:
        # Using a shorter identifier for callback data to avoid length limits
        # We'll use the last 8 characters of the token as a suffix
        token_suffix = clone['bot_token'][-8:]
        btn_text = f"Bot: {clone['bot_token'][:10]}..."
        buttons.append([types.InlineKeyboardButton(btn_text, callback_data=f"edit_clone_{token_suffix}")])

    buttons.append([types.InlineKeyboardButton("Back", callback_data="back_to_supreme")])
    await query.edit_message_text("Select a clone to edit:", reply_markup=types.InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex("^edit_clone_"))
async def edit_clone_cb(client, query):
    if not await db.is_supreme(query.from_user.id):
        return await query.answer("Access Denied", show_alert=True)

    token_suffix = query.data.replace("edit_clone_", "")
    clones = await db.get_clones()
    clone = next((c for c in clones if c['bot_token'].endswith(token_suffix)), None)

    if not clone:
        return await query.answer("Clone not found.", show_alert=True)

    text = f"**Editing Clone**\n\n"
    text += f"Bot Token: `{clone['bot_token']}`\n"
    text += f"API ID: `{clone['api_id']}`\n"
    text += f"API HASH: `{clone['api_hash']}`\n"
    text += f"Assistant Session: `{clone['string_session']}`\n"
    text += f"Owner ID: `{clone['user_id']}`\n\n"
    text += "What would you like to edit?"

    buttons = [
        [
            types.InlineKeyboardButton("Edit Token", callback_data=f"updt_tk_{token_suffix}"),
            types.InlineKeyboardButton("Edit Session", callback_data=f"updt_ss_{token_suffix}"),
        ],
        [
            types.InlineKeyboardButton("Delete Clone", callback_data=f"conf_del_{token_suffix}"),
        ],
        [
            types.InlineKeyboardButton("Back", callback_data="manage_clones"),
        ]
    ]
    await query.edit_message_text(text, reply_markup=types.InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex("^updt_ss_"))
async def update_session_cb(client, query):
    if not await db.is_supreme(query.from_user.id):
        return await query.answer("Access Denied", show_alert=True)

    token_suffix = query.data.replace("updt_ss_", "")
    clones = await db.get_clones()
    clone = next((c for c in clones if c['bot_token'].endswith(token_suffix)), None)

    if not clone:
        return await query.answer("Clone not found.", show_alert=True)

    await query.edit_message_text(f"To update the session for clone `{token_suffix}`, use command:\n`/updt_sess {clone['bot_token']} NEW_SESSION_HERE`")

@Client.on_message(filters.command("updt_sess") & filters.private)
async def updt_sess_command(client, message):
    if not await db.is_supreme(message.from_user.id):
        return await message.reply("Access Denied")

    if len(message.command) < 3:
        return await message.reply("Usage: `/updt_sess [bot_token] [new_session]`")

    bot_token = message.command[1]
    new_session = message.command[2]

    clones = await db.get_clones()
    clone = next((c for c in clones if c['bot_token'] == bot_token), None)

    if not clone:
        return await message.reply("Clone not found.")

    await db.add_clone(bot_token, clone['api_id'], clone['api_hash'], new_session, clone['user_id'])
    await message.reply(f"Session updated for clone `{bot_token[:10]}...`")

@Client.on_callback_query(filters.regex("^updt_tk_"))
async def update_token_cb(client, query):
    if not await db.is_supreme(query.from_user.id):
        return await query.answer("Access Denied", show_alert=True)

    token_suffix = query.data.replace("updt_tk_", "")
    clones = await db.get_clones()
    clone = next((c for c in clones if c['bot_token'].endswith(token_suffix)), None)

    if not clone:
        return await query.answer("Clone not found.", show_alert=True)

    await query.edit_message_text(f"To update the bot token for clone `{token_suffix}`, use command:\n`/updt_tok {clone['bot_token']} NEW_TOKEN_HERE`")

@Client.on_message(filters.command("updt_tok") & filters.private)
async def updt_tok_command(client, message):
    if not await db.is_supreme(message.from_user.id):
        return await message.reply("Access Denied")

    if len(message.command) < 3:
        return await message.reply("Usage: `/updt_tok [old_token] [new_token]`")

    old_token = message.command[1]
    new_token = message.command[2]

    clones = await db.get_clones()
    clone = next((c for c in clones if c['bot_token'] == old_token), None)

    if not clone:
        return await message.reply("Clone not found with provided old token.")

    await db.remove_clone(old_token)
    from bot.plugins.clone import stop_clone
    await stop_clone(old_token)

    await db.add_clone(new_token, clone['api_id'], clone['api_hash'], clone['string_session'], clone['user_id'])
    await message.reply(f"Token updated for clone. Please use `/clone` or restart if it doesn't start automatically.")

@Client.on_callback_query(filters.regex("^conf_del_"))
async def confirm_del_clone_cb(client, query):
    if not await db.is_supreme(query.from_user.id):
        return await query.answer("Access Denied", show_alert=True)

    token_suffix = query.data.replace("conf_del_", "")
    clones = await db.get_clones()
    clone = next((c for c in clones if c['bot_token'].endswith(token_suffix)), None)

    if not clone:
        return await query.answer("Clone not found.", show_alert=True)

    buttons = [
        [
            types.InlineKeyboardButton("Yes, Delete", callback_data=f"real_del_{token_suffix}"),
            types.InlineKeyboardButton("No, Cancel", callback_data=f"edit_clone_{token_suffix}"),
        ]
    ]
    await query.edit_message_text(f"Are you sure you want to delete clone `{token_suffix}`?", reply_markup=types.InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex("^real_del_"))
async def real_del_clone_cb(client, query):
    if not await db.is_supreme(query.from_user.id):
        return await query.answer("Access Denied", show_alert=True)

    token_suffix = query.data.replace("real_del_", "")
    clones = await db.get_clones()
    clone = next((c for c in clones if c['bot_token'].endswith(token_suffix)), None)

    if not clone:
        return await query.answer("Clone already deleted.", show_alert=True)

    from bot.plugins.clone import stop_clone
    await stop_clone(clone['bot_token'])
    await db.remove_clone(clone['bot_token'])

    await query.edit_message_text(f"Clone `{token_suffix}` has been deleted.", reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton("Back to Clones", callback_data="manage_clones")]]))

@Client.on_callback_query(filters.regex("^back_to_supreme$"))
async def back_to_supreme_cb(client, query):
    if not await db.is_supreme(query.from_user.id):
        return await query.answer("Access Denied", show_alert=True)

    buttons = [
        [
            types.InlineKeyboardButton("Manage Clones", callback_data="manage_clones"),
            types.InlineKeyboardButton("Broadcast", callback_data="broadcast_menu"),
        ],
        [
            types.InlineKeyboardButton("Supreme Users", callback_data="manage_supreme"),
        ],
        [
            types.InlineKeyboardButton("Close", callback_data="close_panel"),
        ]
    ]
    await query.edit_message_text("Welcome to the **Supreme Panel**.", reply_markup=types.InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex("^broadcast_menu$"))
async def broadcast_menu_cb(client, query):
    if not await db.is_supreme(query.from_user.id):
        return await query.answer("Access Denied", show_alert=True)

    await query.edit_message_text(
        "**Broadcast System**\n\nTo broadcast a message, reply to the message you want to broadcast with `/broadcast`.",
        reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton("Back", callback_data="back_to_supreme")]])
    )

@Client.on_callback_query(filters.regex("^manage_supreme$"))
async def manage_supreme_cb(client, query):
    if query.from_user.id != config.OWNER_ID:
        return await query.answer("Only Owner can manage Supreme Users.", show_alert=True)

    supremes = await db.get_supreme_users()
    text = "**Supreme Users:**\n\n"
    if not supremes:
        text += "No supreme users added."
    else:
        for user in supremes:
            text += f"- `{user['user_id']}`\n"

    text += "\nTo add: Reply to user with `/addsupreme`"
    text += "\nTo remove: Reply to user with `/remsupreme`"

    await query.edit_message_text(
        text,
        reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton("Back", callback_data="back_to_supreme")]])
    )

@Client.on_callback_query(filters.regex("^close_panel$"))
async def close_panel_cb(client, query):
    await query.message.delete()

# Implement basic broadcast command as well
@Client.on_message(filters.command("broadcast") & filters.private)
async def broadcast_handler(client, message):
    if not await db.is_supreme(message.from_user.id):
        return await message.reply("You don't have Supreme access.")

    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast it.")

    msg = await message.reply("Broadcasting...")

    served_users = await db.get_served_users()
    served_groups = await db.get_served_groups()

    count = 0
    # Broadcast to users
    for user in served_users:
        try:
            await message.reply_to_message.copy(user['user_id'])
            count += 1
            await asyncio.sleep(0.3)
        except Exception:
            pass

    # Broadcast to groups
    for group in served_groups:
        try:
            await message.reply_to_message.copy(group['chat_id'])
            count += 1
            await asyncio.sleep(0.3)
        except Exception:
            pass

    await msg.edit(f"Broadcast completed. Sent to {count} chats.")

@Client.on_message(filters.command("addsupreme") & filters.user(config.OWNER_ID))
async def add_supreme_cmd(client, message):
    if not message.reply_to_message:
        return await message.reply("Reply to a user to give them Supreme powers.")

    user_id = message.reply_to_message.from_user.id
    await db.add_supreme(user_id)
    await message.reply(f"User {user_id} is now a Supreme user.")

@Client.on_message(filters.command("remsupreme") & filters.user(config.OWNER_ID))
async def rem_supreme_cmd(client, message):
    if not message.reply_to_message:
        return await message.reply("Reply to a user to remove their Supreme powers.")

    user_id = message.reply_to_message.from_user.id
    await db.remove_supreme(user_id)
    await message.reply(f"User {user_id}'s Supreme powers removed.")
