from discord.ext import commands
from discord.ext.commands import Cog
from core.context import CustomContext
from core.selfbot import SelfBot

class Hidden(Cog):
    def __init__(self, client: SelfBot) -> None:
        self.client = client

    @commands.command(name='ping', aliases=['p'])
    async def ping(self, ctx: CustomContext) -> None:
        """ Shows the bot's latency """
        await ctx.send_codeblock('md', f'# 🏓 Pong! {round(self.client.latency * 1000)}ms')


async def setup(client: SelfBot) -> None:
    await client.add_cog(Hidden(client))