from __future__ import annotations
from typing import Any, List, Optional, Union
from aiohttp import ClientSession
from discord import Message
from urllib.parse import urlparse
from discord.ext.commands import Context
from discord.guild import BanEntry


class CustomContext(Context):
    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(**kwargs)

    def session(self) -> ClientSession:
        """Returns the bot's aiohttp client session"""
        return self.bot.session

    @staticmethod
    def is_valid_image_url(url: str) -> Optional[str]:
        """Checks if a url leads to an image."""
        types: List[str] = [".png", ".jpg", ".gif", ".bmp", ".webp"]
        parsed: urlparse.ParseResult = urlparse(url)
        if any(parsed.path.endswith(i) for i in types):
            return url.replace(parsed.query, "size=128")
        return None

    async def delete(self) -> Message:
        """Deletes the ctx message"""
        return await self.message.delete()

    async def purge(self, *args, **kwargs) -> List[Message]:
        """Shortcut to channel.purge, preset for selfbot"""
        kwargs.setdefault("bulk", False)
        return await self.channel.purge(*args, **kwargs)

    async def self_purge(self, limit: int = 10) -> List[Message]:
        """Purges selfbot's messages in any channel until limit is reached"""
        deleted_messages: List[Message] = []
        after: Optional[Message] = None
        while len(deleted_messages) < limit:
            async for message in self.channel.history(limit=1000, after=after):
                if message.author.id == self.bot.user.id:
                    try:
                        await message.delete()
                        deleted_messages.append(message)
                        if len(deleted_messages) >= limit:
                            break
                    except:
                        continue
                after = message
            else:
                break
        return deleted_messages

    async def get_ban(self, name_or_id: Union[str, int]) -> Optional[BanEntry]:
        """Helper function to retrieve a banned user"""
        name_or_id = str(name_or_id)
        async for ban in self.guild.bans():
            if name_or_id.isdigit() and ban.user.id == int(name_or_id):
                return ban
            if name_or_id.lower() in str(ban.user).lower():
                return ban
        return None

    async def confirm(self, message: Optional[str] = None) -> bool:
        """Small helper for confirmation messages."""
        await self.send(message or "⚠️ Are you sure you want to proceed? `(Y/N)`")
        resp: Message = await self.bot.wait_for(
            "message",
            check=lambda m: m.author == self.author and m.channel == self.channel,
            timeout=30,
        )
        fals: List[str] = ["n", "no", "false", "0"]
        if resp.content.lower().strip() in fals:
            return False
        return True

    async def send_codeblock(self, language: str, content: str) -> Message:
        """Send a codeblock message"""
        if not content or content.isspace():
            raise ValueError("Message content cannot be empty or only whitespace")
        code_block = f"```{language}\n{content}\n```"
        return await self.send(code_block)

    async def edit_or_send(self, *args, **kwargs) -> Message:
        """If ctx.message exist then edit else send new message"""
        try:
            if getattr(self, "message", None):
                return await self.message.edit(*args, **kwargs)
            else:
                return await self.send(*args, **kwargs)
        except Exception:
            return await self.send(*args, **kwargs)
