from __future__ import annotations
from discord.ext.commands import Cog
from core.selfbot import SelfBot

class NsfwCog(Cog):
    def __init__(self, client: SelfBot) -> None:
        self.client = client

    
async def setup(client: SelfBot) -> None:
    await client.add_cog(NsfwCog(client))
