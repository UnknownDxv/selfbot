from discord import Message
from discord.ext.commands import Bot
from logging import INFO, FileHandler, StreamHandler, getLogger, basicConfig
from core.context import CustomContext
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

# Get logger and prefix
logger = getLogger('SELFBOT')
PREFIX = os.getenv('PREFIX', '..')

# SelfBot class
class SelfBot(Bot):
    def __init__(self, **kwargs: dict) -> None:
        kwargs.setdefault('command_prefix', PREFIX)
        kwargs.setdefault('self_bot', True)
        kwargs.setdefault('chunk_guilds_at_startup', False)
        super().__init__(**kwargs)
        self._sync_presences = False
        self.messages_sent = 0
        self.logger = logger
    
    @staticmethod
    def clear_console() -> None:
        '''Clears the console screen based on the operating system'''
        os.system("cls" if os.name == "nt" else "clear")

    @classmethod
    async def init(cls, token: str) -> None:
        '''Initializes and starts the selfbot with the provided token'''
        async with cls() as client:
            await client.start(token, reconnect=True)

    async def on_ready(self) -> None:
        '''Logs selfbot status and details when connected to Discord'''
        self.clear_console()
        self.logger.info(f'Logged In As {self.user}')
        self.logger.info(f'Loaded {len(self.extensions)} Extensions')
        self.logger.info(f'Default Prefix: {self.command_prefix}')
        self.logger.info(f'Cached Guilds: {len(self.guilds)}')
        self.logger.info(f'Cached Users: {len(self.users)}')
        self.logger.info(f'Latency: {round(self.latency * 1000)}ms')

    async def on_message(self, message: Message) -> None:
        '''Processes only the selfbot's own messages'''
        if message.author.id != self.user.id:
            return
        self.messages_sent += 1
        await self.process_commands(message)

    async def setup_hook(self) -> None:
        '''Loads bot extensions during setup'''
        try:
            await self.load_extension('cogs.hidden')
        except Exception as error:
            self.logger.error(f'Failed to load extension: {error}')

    async def process_commands(self, message: Message) -> None:
        '''Processes commands using a custom context'''
        ctx = await self.get_context(message, cls=CustomContext)
        if ctx.command is None:
            return
        await self.invoke(ctx)