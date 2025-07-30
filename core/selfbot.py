from discord.ext.commands import Bot

__all__ = ['SelfBot']

class SelfBot(Bot):
    def __init__(self):
        super().__init__(command_prefix=(['..']))

    async def setup_hook(self) -> None:
        print('Hello')