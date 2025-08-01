from __future__ import annotations
from typing import Literal
from discord import HTTPException
from discord.ext import commands
from discord.ext.commands import Cog
from core.context import CustomContext
from core.selfbot import SelfBot
import asyncio, random , os

class Utils(Cog):
    def __init__(self, bot: SelfBot) -> None:
        self.bot = bot

    @commands.command(name="hypesquad", description="Change hypesquad house", aliases=['hyp', 'hs'])
    async def change_hypesquad(self, ctx: CustomContext, house: Literal["bravery", "brilliance", "balance"]) -> None:
        '''Change hypesquad house'''
        await ctx.delete()
        ids = {"bravery": 1, "brilliance": 2, "balance": 3}
        api = "https://discord.com/api/v9/hypesquad/online"
        async with ctx.session().post(api, json={"house_id": ids[house]}, headers={"Authorization": os.getenv('TOKEN')}) as res:
            if res.status == 204: await ctx.success()
            else: await ctx.failure()


async def setup(bot: SelfBot) -> None:
    await bot.add_cog(Utils(bot))
