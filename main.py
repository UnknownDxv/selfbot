from logging import getLogger
from discord.errors import LoginFailure
from core.selfbot import SelfBot
import os, asyncio, dotenv
from asyncio import run, sleep

dotenv.load_dotenv()
logger = getLogger('MAIN')
TOKEN = os.getenv('USER_TOKEN')

def setup_env() -> None:
    '''Set up the .env file with user token and prefix.'''
    logger.info("Setting up .env file...")
    os.system("cls" if os.name == "nt" else "clear")
    run(sleep(3))

    input_token = input("Please enter your Discord user token:\n>>> ").strip()
    if not input_token:
        logger.error("No token provided. Exiting setup.")
        exit(1)
    input_prefix = input("Please set your selfbot prefix:\n>>> ").strip()
    env_content = f"USER_TOKEN={input_token}\nPREFIX={input_prefix}\n"

    try:
        with open('.env', 'w') as env_file:
            env_file.write(env_content)
        logger.info("Your .env file created/updated successfully")
    except Exception as e:
        logger.error(f"Failed to create/update .env file: {e}")
        exit(1)

    
async def main() -> None:
    if not os.path.exists('.env') or not TOKEN:
        logger.critical("Your .env file missing or USER_TOKEN not set.")
        setup_env()

    async with SelfBot() as client:
        await client.init(token=TOKEN) 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.critical('Bot stopped by user with Ctrl+C.')
    except LoginFailure as e:
        logger.critical(f'Invalid TOKEN: {e}')
        setup_env()

    