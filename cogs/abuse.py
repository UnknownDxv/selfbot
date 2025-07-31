from __future__ import annotations
from discord import HTTPException
from discord.ext import commands
from discord.ext.commands import Cog
from core.context import CustomContext
from core.selfbot import SelfBot
import asyncio, random


class Abuse(Cog):
    def __init__(self, client: SelfBot) -> None:
        self.client = client

    @commands.command(name="spam", description="Spam  a message multiple times.", aliases=['sp'])
    async def spam(self, ctx: CustomContext, amount: int, delay: int, * , message: str) -> None:
        '''Spam a message multiple times.'''
        if not (3 <= amount <= 100):
            return await ctx.edit_or_send("Amount must be between 3 and 100.", delete_after=5)
        if delay < 0:
            return await ctx.edit_or_send("Delay cannot be negative.", delete_after=5)
        
        await ctx.delete()
        for _ in range(amount):
            try:
                await ctx.send(message)
                await asyncio.sleep(delay)
            except HTTPException as e:
                if e.status == 429:
                    retry_after = getattr(e, "retry_after", 5)
                    await asyncio.sleep(retry_after)
                    await ctx.send(message)

    
async def setup(client: SelfBot) -> None:
    await client.add_cog(Abuse(client))
