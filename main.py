import asyncio
import os
from aiohttp import web
from bot.core.client import bot, assistant
from bot.core.call import call_py
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def health_check(request):
    return web.Response(text="Bot is running")

async def start_server():
    app = web.Application()
    app.add_routes([web.get('/', health_check)])
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"Health check server started on port {port}")

async def main():
    logger.info("Starting Music Bot...")
    await start_server()
    await bot.start()
    logger.info("Bot started.")
    
    if not os.getenv("STRING_SESSION"):
        logger.error("STRING_SESSION is missing. Assistant will not start.")
    else:
        try:
            await assistant.start()
            logger.info("Assistant started.")
        except Exception as e:
            logger.error(f"Failed to start Assistant: {e}")
    
    if assistant.is_connected:
        await call_py.start()
        logger.info("Py-TgCalls started.")
    else:
        logger.warning("Assistant not started, skipping Py-TgCalls.")
    
    logger.info("Bot is idle.")
    from pyrogram import idle
    # Start clones
    from bot.plugins.clone import start_clone
    from bot.database.db import db
    clones = await db.get_clones()
    for clone in clones:
        try:
            await start_clone(clone['bot_token'], clone['api_id'], clone['api_hash'], clone['string_session'])
            logger.info(f"Started clone: {clone['bot_token'][:10]}")
        except Exception as e:
            logger.error(f"Failed to start clone {clone['bot_token'][:10]}: {e}")

    # Import auto_service to start the background tasks
    from bot.services import auto_service
    await idle()

    if assistant.is_connected:
        await call_py.stop()
        await assistant.stop()
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
