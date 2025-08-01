from __future__ import annotations
from typing import Optional
from discord import Emoji, HTTPException, TextChannel, User
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
            await ctx.success()
            await asyncio.sleep(delay_seconds)
        await ctx.send(content='Finished typing!')

    @commands.command(name="emojireact", description="React on the latest message with emojis", aliases=["reactletest"])
    @commands.has_permissions(add_reactions=True)
    async def emojireact(self, ctx: CustomContext, text: str, channel: Optional[TextChannel] = None) -> None:
        '''React on the latest message with emojis'''
        emojis = text_to_emojis(text)
        channel = channel or ctx.channel
        messages = [msg async for msg in channel.history(limit=10) if msg != ctx.message]
        if not messages: return await ctx.failure(content='No messages found in the channel', delete_after=10)
        message = messages[0]
        for emoji in emojis:
            try:
                await message.add_reaction(emoji)
            except HTTPException as e:
                if e.status == 429:
                    retry_after = getattr(e, "retry_after", 5)
                    await asyncio.sleep(retry_after)
                    continue
        await ctx.success()

    @commands.command(name="mreact", description="React on messages in the channel", aliases=[])
    async def mreact(self, ctx: CustomContext, emoji: str, amount: int = 5, channel: Optional[TextChannel] = None) -> None:
        '''React on messages in the channel'''
        if amount < 1 or amount > 25:
            return await ctx.failure(content="Amount must be between 1 and 25.", delete_after=5)
        channel = channel or ctx.channel
        messages = [msg async for msg in channel.history(limit=amount+1) if msg != ctx.message]
        if not messages:
            return await ctx.failure(content="No messages found to react to.", delete_after=5)
        success_count = 0
        for message in messages[:amount]:
            try:
                await message.add_reaction(emoji)
                success_count += 1
            except HTTPException as e:
                if e.status == 429:
                    retry_after = getattr(e, "retry_after", 5)
                    await asyncio.sleep(retry_after)
                    continue
        await ctx.send(content=f"Reacted to {success_count} message(s) with {emoji}.")
        
    @commands.command(name="tts", description="Text to speech message", aliases=[])
    async def tts(self, ctx: CustomContext, *, text: str) -> None:
        '''Text to speech message'''
        await ctx.success(delete=True)
        await ctx.send(content=text, tts=True)

async def setup(bot: SelfBot) -> None:
    await bot.add_cog(Fun(bot))
