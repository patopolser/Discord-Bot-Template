import logging
import os

import discord
from discord.ext import commands

from bot import (
    PREFIX, 
    DESCRIPTION,
    TOKEN, 
    NAME, 
    VERSION
)
from bot.ext import HelpCommand
from bot.utils import Checks, Embeds

log = logging.getLogger(__name__)

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix= PREFIX,
            description= DESCRIPTION,
            help_command= HelpCommand(),
            case_insensitive= True,
            intents= discord.Intents.all()
        )
        self.add_command(self.reload)
        self.load_extensions()

    async def on_ready(self) -> None:
        log.info(f"{NAME} v{VERSION} Started - Logged as {self.user}")
        
    @commands.command()
    @Checks.is_developer()
    async def reload(ctx: commands.Context) -> None:
        for extension in ctx.bot.extensions:
            ctx.bot.reload_extension(extension)

        await ctx.message.delete()

    async def on_application_command_error(self, ctx: discord.ApplicationContext, error):

        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.respond(embed= Embeds.error_embeds(f"Usage: `{PREFIX}{ctx.command.name} {ctx.command.signature}`", "Missing required argument"))

        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.respond(embed= Embeds.error_embeds(f"{ctx.author.mention} Command not found, use `{PREFIX}help`", "Command Not Found"))

        elif isinstance(error, commands.errors.BadArgument):
            await ctx.respond(embed = Embeds.error_embeds(f"{ctx.author.mention} Bad Argument, use `{PREFIX}help {ctx.command.name}`", "Bad Argument"))

        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.respond(embed = Embeds.error_embeds(f"{ctx.author.mention} You don't have the required permissions", "Missing Permissions"))

        elif isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.respond(embed = Embeds.error_embeds(f"{ctx.author.mention} {error.args[0]}", "Cooldown Error"))

        elif isinstance(error, commands.errors.CheckFailure):
            await ctx.respond(embed = Embeds.error_embeds(f"{ctx.author.mention} You don't have the required permissions", "Check error"))

        elif isinstance(error, discord.errors.ApplicationCommandInvokeError):
            log.warning(error)
            await ctx.respond(embed = Embeds.error_embeds(f"{ctx.author.mention} Command Invoke Error. Please report it", "Command Invoke Error"))
        
        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.respond(embed = Embeds.error_embeds(f"{ctx.author.mention} Member not found", "Member Not Found"))

        elif isinstance(error, commands.errors.RoleNotFound):
            await ctx.respond(embed = Embeds.error_embeds(f"{ctx.author.mention} Role not found", "Role Not Found"))

        elif isinstance(error, commands.errors.ChannelNotFound):
            await ctx.respond(embed = Embeds.error_embeds(f"{ctx.author.mention} Channel not found", "Channel Not Found"))
       
        else:
            log.warning(f"{NAME}.{__class__.__name__} module error: {error}")

    def run(self) -> None:
        return super().run(TOKEN, reconnect= True)

    def load_extensions(self) -> None:
        for i in os.listdir("./bot/modules"):
            if i.endswith(".py"):
                self.load_extension(f"bot.modules.{i[:-3]}")