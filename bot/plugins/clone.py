import os
import asyncio
from pyrogram import Client, filters
from bot.core.client import bot
from bot.database.db import db
from bot.config.config import config

CLONE_CLIENTS = {}
ASSISTANT_CLIENTS = {}

async def start_clone(bot_token, api_id, api_hash, string_session):
    if bot_token in CLONE_CLIENTS:
        return CLONE_CLIENTS[bot_token]

    clone_bot = Client(
        f"Clone_{bot_token[:10]}",
        api_id=api_id,
        api_hash=api_hash,
        bot_token=bot_token,
        plugins=dict(root="bot/plugins")
    )

    clone_assistant = Client(
        f"Assistant_{bot_token[:10]}",
        api_id=api_id,
        api_hash=api_hash,
        session_string=string_session
    )

    await clone_bot.start()
    await clone_assistant.start()

    CLONE_CLIENTS[bot_token] = clone_bot
    ASSISTANT_CLIENTS[bot_token] = clone_assistant
    return clone_bot

async def stop_clone(bot_token):
    stopped = False
    if bot_token in CLONE_CLIENTS:
        client = CLONE_CLIENTS.pop(bot_token)
        await client.stop()
        stopped = True

    if bot_token in ASSISTANT_CLIENTS:
        assistant_client = ASSISTANT_CLIENTS.pop(bot_token)
        await assistant_client.stop()
        stopped = True

    return stopped

@bot.on_message(filters.command("clone") & filters.private)
async def clone_bot_handler(_, message):
    if len(message.command) < 5:
        return await message.reply(
            "**Usage:**\n/clone [bot_token] [api_id] [api_hash] [string_session]"
        )

    bot_token = message.command[1]
    try:
        api_id = int(message.command[2])
    except ValueError:
        return await message.reply("API_ID must be an integer.")
    api_hash = message.command[3]
    string_session = message.command[4]

    msg = await message.reply("Starting your clone bot...")

    try:
        await db.add_clone(bot_token, api_id, api_hash, string_session, message.from_user.id)
        await start_clone(bot_token, api_id, api_hash, string_session)
        await msg.edit(f"**Clone Bot Started!**\n\nYour bot is now running with the provided configuration.")
    except Exception as e:
        await msg.edit(f"**Error:** {e}")

@bot.on_message(filters.command("clones") & filters.user(config.OWNER_ID))
async def list_clones(_, message):
    clones = await db.get_clones()
    if not clones:
        return await message.reply("No clones running.")

    text = "**Active Clones:**\n\n"
    for clone in clones:
        text += f"- Token: `{clone['bot_token'][:10]}...` (User: {clone['user_id']})\n"

    await message.reply(text)

@bot.on_message(filters.command("delclone") & filters.user(config.OWNER_ID))
async def del_clone_handler(_, message):
    if len(message.command) < 2:
        return await message.reply("**Usage:** /delclone [bot_token]")

    bot_token = message.command[1]
    await db.remove_clone(bot_token)
    stopped = await stop_clone(bot_token)

    if stopped:
        await message.reply("Clone stopped and removed.")
    else:
        await message.reply("Clone removed from DB, but it wasn't running.")
