from __future__ import annotations
from discord.ext import commands
from discord import DiscordException
from discord.ext.commands import Cog
from core.context import CustomContext
from core.selfbot import SelfBot
import time

class Error(Cog):
    def __init__(self, bot: SelfBot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: CustomContext, error: DiscordException) -> None:
        '''Handle all errors raised during command execution'''
        if hasattr(error, 'handled') and error.handled:
            return 

        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f'Check Failure: {str(error)}', delete_after=10)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'Missing Argument: `<{error.param.name}>` is required!', delete_after=10)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f'Invalid Argument: {str(error)}', delete_after=10)
        elif isinstance(error, commands.BadLiteralArgument):
            await ctx.send(f'Invalid Literal Argument: Expected one of: {", ".join(error.literals)}', delete_after=10)
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('I do not have permission to use this command!', delete_after=10)
        elif isinstance(error, commands.CommandOnCooldown):
            retry_timestamp = int(time.time() + error.retry_after)
            await ctx.send(f'Command on cooldown. Try again <t:{retry_timestamp}:R>', delete_after=error.retry_after)
        elif isinstance(error, commands.NotOwner):
            await ctx.send('This command is restricted to the bot owner!', delete_after=10)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f'Missing Permissions: {", ".join(error.missing_permissions)}', delete_after=10)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f'Bot Missing Permissions: {", ".join(error.missing_permissions)}', delete_after=10)
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send('This command is currently disabled!', delete_after=10)
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send('Too many arguments provided for this command!', delete_after=10)
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('This command cannot be used in DMs!', delete_after=10)
        elif isinstance(error, commands.MissingRole):
            await ctx.send(f'Missing required role: {error.missing_role}', delete_after=10)
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send(f'Missing one of required roles: {", ".join(error.missing_roles)}', delete_after=10)
        elif isinstance(error, commands.BotMissingRole):
            await ctx.send(f'Bot missing required role: {error.missing_role}', delete_after=10)
        elif isinstance(error, commands.BotMissingAnyRole):
            await ctx.send(f'Bot missing one of required roles: {", ".join(error.missing_roles)}', delete_after=10)
        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.send('This command can only be used in NSFW channels!', delete_after=10)
        else:
            self.bot.logger.error(f'Unhandled error: {error.__class__.__name__}: {str(error)}')

async def setup(bot: SelfBot) -> None:
    await bot.add_cog(Error(bot))