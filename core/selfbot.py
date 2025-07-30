from discord.ext import commands

__all__ = ['SelfBot']

class SelfBot(commands.Bot):
    def __init__(self, PREFIX: str):
        super().__init__(command_prefix=PREFIX)

    async def setup_hook(self) -> None:
        print('Hello')