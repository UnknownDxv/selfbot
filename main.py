from core import SelfBot
import os, asyncio, dotenv
from core import logger

dotenv.load_dotenv()
TOKEN = os.getenv('USER_TOKEN')

async def main() -> None:
    async with SelfBot() as client:
        await client.start(token=TOKEN, reconnect=True) 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Bot stopped by user with Ctrl+C.')
    