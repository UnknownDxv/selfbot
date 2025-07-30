from discord.ext.commands import Bot
from logging import INFO, FileHandler, StreamHandler, getLogger, basicConfig
import os

# Make logs directory if it doesn't exist
os.makedirs(name='logs', exist_ok=True)

# Configure logger
logger = basicConfig(
    level=INFO,
    datefmt='%d-%m-%Y %H:%M:%S',
    format='%(asctime)s - [%(name)s] - [%(levelname)s]: %(message)s',
    handlers=[FileHandler('logs/selfbot.log', 'a', 'utf-8'), StreamHandler()]
)

# Get logger
logger = getLogger('SELFBOT')

# SelfBot class
class SelfBot(Bot):
    def __init__(self, **kwargs: dict) -> None:
        super().__init__(command_prefix=(['..']), **kwargs)
        self._sync_presences = False
        self.logger = logger
    
    @staticmethod
    def clear_console() -> None:
        """ Clear console """
        os.system("cls" if os.name == "nt" else "clear")

    @classmethod
    async def init(cls, token: str)-> None:
        """ Initialize selfbot """
        async with cls() as client:
            await client.start(token, reconnect=True)

    async def setup_hook(self) -> None:
        """ Setup hook """
        await self.load_extension('cogs.hidden')
        self.logger.info(f'Loaded {len(self.extensions)} Extensions')

    async def on_ready(self) -> None:
        """ On ready event"""
        self.logger.info(f'Logged in as {self.user}')