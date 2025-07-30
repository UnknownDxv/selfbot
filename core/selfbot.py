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
        super().__init__(command_prefix=(['..']), self_bot=True, **kwargs)
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

    async def on_ready(self) -> None:
        """ On ready event"""
        self.clear_console()
        self.logger.info(f'Logged In As {self.user}')
        self.logger.info(f'Loaded {len(self.extensions)} Extensions')
        self.logger.info(f'Default Prefix: {self.command_prefix}')
        self.logger.info(f'Cached Guilds: {len(self.guilds)}')
        self.logger.info(f'Cached Users: {len(self.users)}')
        self.logger.info(f'Latency: {round(self.latency * 1000)}ms')

    async def setup_hook(self) -> None:
        """ Setup hook """
        try:
            await self.load_extension('cogs.hidden')
        except Exception as error:
            self.logger.error(f'Failed to load extension: {error}')
