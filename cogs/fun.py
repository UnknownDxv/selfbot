from __future__ import annotations
from discord.ext import commands
from discord.ext.commands import Cog
from core.context import CustomContext
from core.selfbot import SelfBot


class Fun(Cog):
    def __init__(self, client: SelfBot) -> None:
        self.client = client

    @commands.command(
        name="8ball",
        description="Get an answer to your question",
        aliases=["8b", "ask", "eightball"],
        usage="<question>",
    )
    async def _8ball(self, ctx: CustomContext, *, question: str) -> None:
        pass


async def setup(client: SelfBot) -> None:
    await client.add_cog(Fun(client))
