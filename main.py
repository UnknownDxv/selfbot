from __future__ import annotations
from logging import getLogger
from typing import Any
from discord.errors import LoginFailure
from core.selfbot import SelfBot
import asyncio, dotenv

# Load environment variables
dotenv.load_dotenv()

# Setup logger
logger = getLogger("MAIN")

async def main(**kwargs: dict[str, Any]) -> None:
    self_bot = SelfBot()
    token = self_bot.token
    try:
        await self_bot.start(token, **kwargs)
    except LoginFailure as e:
        logger.critical(f"Invalid TOKEN: {e}")
        self_bot.run_wizard()
    finally:
        await self_bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main(reconnect=True))
    except KeyboardInterrupt:
        logger.critical("Bot stopped by user with Ctrl+C.")