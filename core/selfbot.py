from __future__ import annotations
from aiohttp import ClientSession
from discord import Message
from discord.ext.commands import Bot
from logging import INFO, FileHandler, StreamHandler, getLogger, basicConfig
from core.context import CustomContext
import os, shutil, sys

# Make logs directory if it doesn't exist
os.makedirs(name="logs", exist_ok=True)

# Configure logger
logger = basicConfig(
    level=INFO,
    datefmt="%d-%m-%Y %H:%M:%S",
    format="%(asctime)s - [%(name)s] - [%(levelname)s]: %(message)s",
    handlers=[FileHandler("logs/selfbot.log", "a", "utf-8"), StreamHandler()],
)

# Get logger 
logger = getLogger("SELFBOT")

# TOKEN and PREFIX from env
TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX", "..")


# SelfBot class
class SelfBot(Bot):
    def __init__(self, **kwargs: dict) -> None:

        kwargs.setdefault("command_prefix", PREFIX)
        kwargs.setdefault("self_bot", True)
        kwargs.setdefault("chunk_guilds_at_startup", False)
        kwargs.setdefault("case_insensitive", True)
        kwargs.setdefault("strip_after_prefix", True)
        kwargs.setdefault("help_command", None)
        kwargs.setdefault("sync_presence", True)

        super().__init__(**kwargs)
        self.session = ClientSession()
        self.messages_sent = 0
        self.logger = logger

    @property
    def token(self) -> str:
        '''Returns your token wherever it is'''
        token = os.getenv("TOKEN")
        if token is None:
            self.run_wizard()
        else:
            return token.strip('"')
    
    @staticmethod
    def run_wizard():
        '''Wizard for first start'''
        print('-' * shutil.get_terminal_size().columns)
        input_token = input("Please enter your discord user token:\n>>> ").strip('\"')
        print('-' * shutil.get_terminal_size().columns)
        input_prefix = input("Please set your selfbot prefix:\n>>> ").strip('\"')
        env_content = f"TOKEN={input_token}\nPREFIX={input_prefix}\n"

        with open(".env", "w") as env_file:
            env_file.write(env_content)

        os.system("cls" if os.name == "nt" else "clear")
        print('-' * shutil.get_terminal_size().columns)
        print('Restarting...')
        print('-' * shutil.get_terminal_size().columns)
        os.execv(sys.executable, ['python'] + sys.argv)

    @staticmethod
    def clear_console() -> None:
        '''Clears the console screen based on the operating system'''
        os.system("cls" if os.name == "nt" else "clear")

    async def on_ready(self) -> None:
        '''Logs selfbot status and details when connected to Discord'''
        self.clear_console()
        self.logger.info(f"Logged In As @{self.user} ({self.user.id})")
        self.logger.info(f"Loaded {len(self.extensions)} Extensions")
        self.logger.info(f"Default Prefix: {self.command_prefix}")
        self.logger.info(f"Cached Guilds: {len(self.guilds)}")
        self.logger.info(f"Cached Members: {sum(g.member_count for g in self.guilds)}")
        self.logger.info(f"Latency: {round(self.latency * 1000)}ms")

    async def on_message(self, message: Message) -> None:
        '''Processes only the selfbot's own messages'''
        if message.author.id != self.user.id: return
        self.messages_sent += 1
        await self.process_commands(message)

    async def setup_hook(self) -> None:
        '''Loads bot extensions during setup'''
        await self.load_extension("cogs.abuse")
        await self.load_extension("cogs.error")
        await self.load_extension("cogs.fun")
        await self.load_extension("cogs.utils")
        await self.load_extension("cogs.troll")

    async def process_commands(self, message: Message) -> None:
        '''Processes commands using a custom context'''
        ctx = await self.get_context(message, cls=CustomContext)
        if ctx.command is None: return
        await self.invoke(ctx)

