import logging

from discord.ext import commands

from bot import NAME

log = logging.getLogger(__name__)

class Default(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(f"{NAME}.{__class__.__name__} loaded")


def setup(bot):
    bot.add_cog(Default(bot))