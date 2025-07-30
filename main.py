from logging import getLogger
from core import SelfBot
import os, asyncio, dotenv

dotenv.load_dotenv()
logger = getLogger('MAIN')
TOKEN = os.getenv('USER_TOKEN')

async def main() -> None:
    async with SelfBot() as client:
        await client.init(token=TOKEN) 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.critical('Bot stopped by user with Ctrl+C.')
    