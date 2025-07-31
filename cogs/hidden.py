from discord.ext import commands
from discord.ext.commands import Cog
from core.context import CustomContext
from core.selfbot import SelfBot

class Hidden(Cog):
    def __init__(self, client: SelfBot) -> None:
        self.client = client

    @commands.command(aliases=['pong'])
    async def ping(self, ctx: CustomContext) -> None:
        ''' Shows the bot's latency '''
        await ctx.edit_or_send(f'🏓 Pong! {round(self.client.latency * 1000)}ms', delete_after=10)

async def setup(client: SelfBot) -> None:
    await client.add_cog(Hidden(client))