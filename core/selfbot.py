from discord.ext.commands import Bot
from logging import INFO, FileHandler, StreamHandler, getLogger, basicConfig
import os

logger = basicConfig(
    level=INFO,
    datefmt='%d-%m-%Y %H:%M:%S',
    format='%(asctime)s - [%(name)s] - [%(levelname)s]: %(message)s',
    handlers=[FileHandler('logs/selfbot.log', 'a', 'utf-8'), StreamHandler()]
)

logger = getLogger('SELFBOT')


class SelfBot(Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=['..'])
        self._sync_presences = False
        self.logger = logger
    
    @staticmethod
    def clear_console() -> None:
        os.system("cls" if os.name == "nt" else "clear")

    async def setup_hook(self) -> None:
        self.wait_until_ready()
        self.clear_console()