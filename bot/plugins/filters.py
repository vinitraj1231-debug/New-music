from pyrogram import filters
from bot.core.client import bot
from bot.services.filter_service import filter_service

@bot.on_message(filters.command(["bass", "nightcore", "slowed", "deep", "8d"]) & filters.group)
async def filter_command(_, message):
    cmd = message.command[0]
    # In a real implementation, we would restart the stream with this filter applied to FFmpeg
    await message.reply(f"Filter {cmd} applied (simulated).")

@bot.on_message(filters.command("filter") & filters.group)
async def list_filters(_, message):
    text = "**Available Filters:**\n\n- /bass\n- /nightcore\n- /slowed\n- /deep\n- /8d"
    await message.reply(text)
