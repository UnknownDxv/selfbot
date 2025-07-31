from __future__ import annotations
import asyncio
from discord import HTTPException
from discord.ext import commands
from discord.ext.commands import Cog
from core.context import CustomContext
from core.selfbot import SelfBot
import random


class FunCog(Cog):
    def __init__(self, client: SelfBot) -> None:
        self.client = client

    @commands.command(
        name="8ball",
        description="Get an answer to your question",
        aliases=["8b", "ask", "eightball"],
        usage="8ball <question>",
    )
    async def _8ball(self, ctx: CustomContext, *, question: str) -> None:
        """Get an answer to your question"""
        responses = [
            "It is certain.",
            "Without a doubt.",
            "You may rely on it.",
            "Yes – definitely.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]
        answer = random.choice(responses)
        await ctx.delete()
        await ctx.send(f"🎱 **Question:** {question} **Answer:** {answer}")

    @commands.command(
        name="spam",
        description="Spam  a message multiple times.",
        aliases=['sp'],
        usage="<message> <amount> <delay>"
    )
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
    await client.add_cog(FunCog(client))
