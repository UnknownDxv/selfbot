from __future__ import annotations
from typing import Optional
from discord import HTTPException, TextChannel, User
from discord.ext import commands
from discord.ext.commands import Cog
from core.context import CustomContext
from core.selfbot import SelfBot
import asyncio, random

from utils.convert import text_to_emojis


class Fun(Cog):
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

    @commands.command(name="deathdate", description="Predicted death date", aliases=["dd", "death"])
    async def deathdate(self, ctx: CustomContext, user: Optional[User] = None) -> None:
        '''Predicted death date'''
        await ctx.success(delete=True)
        await ctx.send(f"☠️ **{user}** will die in {random.randint(1, 90)} years")

    @commands.command(name="triggertyping", description="Show your self typing in the chat", aliases=["tt", "typing"])
    async def triggertyping(self, ctx: CustomContext, delay_seconds: Optional[int] = 60, channel: Optional[TextChannel] = None) -> None:
        '''Show your self typing in the chat'''
        channel = channel or ctx.channel
        async with channel.typing():
            await asyncio.sleep(delay_seconds)
        await ctx.success()

    @commands.command(name="emojireact", description="React on the latest message with emojis", aliases=["reactletest"])
    @commands.has_permissions(add_reactions=True)
    async def emojireact(self, ctx: CustomContext, text: str, channel: Optional[TextChannel] = None) -> None:
        '''React on the latest message with emojis'''
        emojis = text_to_emojis(text)
        channel = channel or ctx.channel
        messages = [msg async for msg in channel.history(limit=10)]
        if not messages: return await ctx.failure('No messages found in the channel')
        message = messages[0]
        for emoji in emojis:
            try:
                await message.add_reaction(emoji)
            except HTTPException:
                continue
        await ctx.success()


async def setup(bot: SelfBot) -> None:
    await bot.add_cog(Fun(bot))
