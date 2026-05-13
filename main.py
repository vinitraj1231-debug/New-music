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

async def start_assistant():
    if not os.getenv("STRING_SESSION"):
        logger.error("STRING_SESSION is missing. Assistant will not start.")
        return

    try:
        logger.info("Starting Assistant...")
        await asyncio.wait_for(assistant.start(), timeout=60)
        logger.info("Assistant started.")

        await call_py.start()
        logger.info("Py-TgCalls started.")
    except asyncio.TimeoutError:
        logger.error("Assistant startup timed out.")
    except Exception as e:
        if "unpack requires a buffer of" in str(e):
            logger.error("Invalid STRING_SESSION: Failed to unpack session string.")
        else:
            logger.error(f"Failed to start Assistant: {e}")

async def start_clones_task():
    from bot.plugins.clone import start_clone
    from bot.database.db import db
    try:
        logger.info("Fetching clones from database...")
        clones = await db.get_clones()
        logger.info(f"Found {len(clones)} clones. Starting...")
        for clone in clones:
            try:
                await start_clone(clone['bot_token'], clone['api_id'], clone['api_hash'], clone['string_session'])
                logger.info(f"Started clone: {clone['bot_token'][:10]}...")
            except Exception as e:
                logger.error(f"Failed to start clone {clone['bot_token'][:10]}...: {e}")
    except Exception as e:
        logger.error(f"Database error while fetching clones: {e}")

async def main():
    logger.info("Starting Music Bot...")
    await start_server()

    logger.info("Starting Main Bot...")
    await bot.start()
    logger.info("Main Bot started.")

    # Start Assistant and Clones in background to avoid blocking main bot
    asyncio.create_task(start_assistant())
    asyncio.create_task(start_clones_task())

    # Start the background services
    from bot.services import auto_service
    await auto_service.start()

    logger.info("Bot is idle and responding to commands.")
    from pyrogram import idle
    await idle()

    # Shutdown
    if assistant.is_connected:
        try:
            await call_py.stop()
        except:
            pass
        await assistant.stop()
    await bot.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
