from pyrogram.types import CallbackQuery
from bot.core.client import bot
from bot.core.call import call_py
from bot.services.playback_service import playback_service

@bot.on_callback_query()
async def cb_handler(_, query: CallbackQuery):
    if query.data == "pause":
        try:
            await call_py.pause(query.message.chat.id)
            await query.answer("Paused")
        except Exception:
            await query.answer("Error pausing", show_alert=True)
    elif query.data == "resume":
        try:
            await call_py.resume(query.message.chat.id)
            await query.answer("Resumed")
        except Exception:
            await query.answer("Error resuming", show_alert=True)
    elif query.data == "skip":
        res = await playback_service.skip(query.message.chat.id)
        if res:
            await query.answer("Skipped")
        else:
            await query.answer("Queue empty or error")
    elif query.data == "stop":
        await playback_service.stop(query.message.chat.id)
        await query.answer("Stopped")
        await query.message.edit("Playback stopped.")
