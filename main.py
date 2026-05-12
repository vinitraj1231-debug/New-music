import asyncio
from bot.core.client import bot, assistant
from bot.core.call import call_py
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting Music Bot...")
    await bot.start()
    logger.info("Bot started.")
    
    await assistant.start()
    logger.info("Assistant started.")
    
    await call_py.start()
    logger.info("Py-TgCalls started.")
    
    logger.info("Bot is idle.")
    from pyrogram import idle
    # Import auto_service to start the background tasks
    from bot.services import auto_service
    await idle()

    await call_py.stop()
    await assistant.stop()
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
