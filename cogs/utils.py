from __future__ import annotations
from typing import Literal
from discord import HTTPException
from discord.ext import commands
from discord.ext.commands import Cog
from core.context import CustomContext
from core.selfbot import SelfBot
import asyncio, random , os

class Utils(Cog):
    def __init__(self, client: SelfBot) -> None:
        self.client = client

    @commands.command(name="hypesquad", description="Change hypesquad house", aliases=['hyp', 'hs'])
    async def change_hypesquad(self, ctx: CustomContext, house: Literal["bravery", "brilliance", "balance"]) -> None:
        '''Change hypesquad house'''
        await ctx.delete()
        ids = {"bravery": 1, "brilliance": 2, "balance": 3}
        api = "https://discord.com/api/v9/hypesquad/online"
        async with ctx.session().post(api, json={"house_id": ids[house]}, headers={"Authorization": os.getenv('USER_TOKEN')}) as res:
            if res.status == 204: await ctx.send('✅')
            else: await ctx.send('❌')



async def setup(client: SelfBot) -> None:
    await client.add_cog(Utils(client))
