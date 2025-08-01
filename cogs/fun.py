from __future__ import annotations
from discord import HTTPException
from discord.ext import commands
from discord.ext.commands import Cog
from core.context import CustomContext
from core.selfbot import SelfBot
import asyncio, random


class FunCog(Cog):
    def __init__(self, bot: SelfBot) -> None:
        self.bot = bot

    @commands.command(name="8ball", description="Get an answer to your question", aliases=["8b", "ask", "eightball"])
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
        await ctx.success(delete=True)
        await ctx.send(f"🎱 **Question:** {question} **Answer:** {answer}")



async def setup(bot: SelfBot) -> None:
    await bot.add_cog(FunCog(bot))
