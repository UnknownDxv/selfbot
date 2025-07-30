from discord.ext.commands import Cog
from core import SelfBot


class Hidden(Cog):
    def __init__(self, client: SelfBot) -> None:
        self.client = client

async def setup(client: SelfBot) -> None:
    await client.add_cog(Hidden(client))