from discord.ext import commands

from bot import GUILD_ID, DEVELOPERS

class Checks:
    
    def is_developer():
        async def check(ctx):
            return ctx.author.id in DEVELOPERS
        
        return commands.check(check)

    def is_bot_guild():
        async def check(ctx):
            return ctx.guild.id == GUILD_ID

        return commands.check(check)