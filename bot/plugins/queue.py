from pyrogram import filters
from bot.core.client import bot
from bot.services.queue_service import queue_service

@bot.on_message(filters.command("queue") & filters.group)
async def queue_command(_, message):
    queue = await queue_service.get_queue(message.chat.id)
    if not queue:
        return await message.reply("The queue is empty.")

    text = "**Current Queue:**\n\n"
    for i, song in enumerate(queue):
        text += f"{i+1}. {song['title']}\n"
        if i == 9: # Limit to 10 for brevity
            text += f"... and {len(queue) - 10} more."
            break

    await message.reply(text)

@bot.on_message(filters.command("shuffle") & filters.group)
async def shuffle_command(_, message):
    await queue_service.shuffle_queue(message.chat.id)
    await message.reply("🔀 Queue shuffled.")
