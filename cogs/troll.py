from __future__ import annotations
from typing import Optional
from discord import Emoji, HTTPException, TextChannel, User
from discord.audit_logs import F
from discord.ext import commands
from discord.ext.commands import Cog
from core.context import CustomContext
from core.selfbot import SelfBot
import asyncio, random, discord

class Troll(Cog):
    def __init__(self, bot: SelfBot) -> None:
        self.bot = bot 


async def setup(bot: SelfBot) -> None:
    await bot.add_cog(Troll(bot))