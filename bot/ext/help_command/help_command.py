import asyncio
import datetime
import random

import discord
from discord.ext import commands

from discord.interactions import Interaction
from discord.ui import (
    Select, 
    Button, 
    View
)

from bot import (
    PREFIX,
    AVATAR,
    COLORS,
    VERSION
)
from .paginator import Paginator

cogs_emojis = {
    "all": "🌎",
    "default": "🔑",
}

class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                'help': 'Shows help about a command or a module'
            }
        )
    
    def get_cog(self, cog_name):
        return self.context.bot.cogs[cog_name]

    def get_embed(self, paginator: Paginator, cog, bot):
        embed = discord.Embed(
            title= f"{cog} Commands",
            description= f"Page {paginator.actual_page + 1}/{len(paginator.pages)}",
            color= random.choice(COLORS)
        )
        embed.set_author(name= bot.display_name, icon_url= bot.avatar)
        embed.set_footer(text = f"v{VERSION}", icon_url= AVATAR)
        embed.timestamp = datetime.datetime.utcnow()
        
        commands = paginator.current_page
        for command in commands:
            embed.add_field(
                name= f"{PREFIX}{command.name} {command.signature}",
                value= f"⚔️ {command.description}",
                inline= False
            )

        return embed
        

    async def send_bot_help(self, mapping: list):
        ctx = self.context
        bot = ctx.bot
        
        select_options = [
            discord.SelectOption(
                label= cog.qualified_name, 
                value= cog.qualified_name, 
                emoji= cogs_emojis[cog.qualified_name.lower()]
            ) 
            for cog in mapping if cog is not None and len(cog.get_commands())
            ]
        select_options.insert(0, discord.SelectOption(label="All", value="All", emoji= cogs_emojis["all"]))

        select_menu = Select(placeholder="Select a module", options= select_options)

        button_left = Button(emoji= "◀️", custom_id= "left", style= discord.ButtonStyle.blurple)
        button_right = Button(emoji= "▶️", custom_id= "right", style= discord.ButtonStyle.blurple)

        view = View(button_left, button_right, select_menu)

        all_commands = []
        for cog in mapping:
            if cog is not None:
                all_commands += cog.get_commands()

        all_commands = await self.filter_commands(all_commands, sort= True)
        paginator = Paginator(all_commands)
        actual_cog = "All"
        
        embed = self.get_embed(paginator, actual_cog, self.context.bot.user)
        message = await ctx.send(embed= embed, view= view)

        while True:
            if len(paginator.pages) == paginator.actual_page + 1:
                button_right.disabled = True
            else:
                button_right.disabled = False

            if not paginator.actual_page:
                button_left.disabled = True
            else:
                button_left.disabled = False
            
            await message.edit(embed= embed, view= View(button_left, button_right, select_menu))

            try:
                interaction: Interaction = await bot.wait_for(
                    "interaction", 
                    check= lambda m: m.user == ctx.author and m.channel == ctx.channel, 
                    timeout= 20
                )
                await interaction.response.defer()
            
            except asyncio.TimeoutError:
                button_right.disabled = True
                button_left.disabled = True
                select_menu.disabled = True

                await message.edit(embed= embed, view= View(button_left, button_right, select_menu))
                return

            if interaction.data["custom_id"] == "right":
                paginator.next_page()
                embed = self.get_embed(paginator, actual_cog, bot.user)

            elif interaction.data["custom_id"] == "left":
                paginator.previous_page()
                embed = self.get_embed(paginator, actual_cog, bot.user)

            else:
                current_module = interaction.data["values"][0]
                
                if current_module == "All":
                    actual_cog = "All"
                    paginator = Paginator(all_commands)
                else:
                    module = self.get_cog(current_module)
                    actual_cog = module.qualified_name
                    paginator = Paginator(await self.filter_commands(module.get_commands(), sort= True))

                embed = self.get_embed(paginator, actual_cog, bot.user)
        
            await message.edit(embed= embed, view= View(button_left, button_right, select_menu))


    async def send_cog_help(self, cog):
        ctx = self.context
        bot = self.context.bot

        if not cog.get_commands():
            await ctx.send("Cog has no commands")
            return

        button_left = Button(emoji= "◀️", custom_id= "left", style= discord.ButtonStyle.blurple)
        button_right = Button(emoji= "▶️", custom_id= "right", style= discord.ButtonStyle.blurple)

        view = View(button_left, button_right)

        cog_commands = await self.filter_commands(cog.get_commands(), sort= True)
        paginator = Paginator(cog_commands)

        embed = self.get_embed(paginator, cog.qualified_name, self.context.bot.user)
        message = await ctx.send(embed= embed, view= view)

        while True:
            if len(paginator.pages) == paginator.actual_page + 1:
                button_right.disabled = True
            else:
                button_right.disabled = False

            if not paginator.actual_page:
                button_left.disabled = True
            else:
                button_left.disabled = False
            
            await message.edit(embed= embed, view= View(button_left, button_right))

            try:
                interaction: Interaction = await bot.wait_for(
                    "interaction", 
                    check= lambda m: m.user == ctx.author and m.channel == ctx.channel, 
                    timeout= 20
                )
                await interaction.response.defer()
            
            except asyncio.TimeoutError:
                button_right.disabled = True
                button_left.disabled = True

                await message.edit(embed= embed, view= View(button_left, button_right))
                return

            if interaction.data["custom_id"] == "right":
                paginator.next_page()
                embed = self.get_embed(paginator, cog.qualified_name, bot.user)

            elif interaction.data["custom_id"] == "left":
                paginator.previous_page()
                embed = self.get_embed(paginator, cog.qualified_name, bot.user)

            await message.edit(embed= embed, view= View(button_left, button_right))


    async def send_command_help(self, command):

        aliases = command.name if not command.aliases else ", ".join(command.aliases)
        
        embed = discord.Embed(
            title= f"{str(command.name).capitalize()} Help", 
            description= f"{command.description}", 
            color = random.choice(COLORS)
        )

        embed.set_thumbnail(url= AVATAR)
        embed.set_footer(text = "Syntax: <required_args> [optional_args]", icon_url= AVATAR)
        embed.add_field(name= "Usage", value= f"{PREFIX}{command} {command.signature}", inline= False)
        embed.add_field(name= "Module", value= f"{command.cog_name}", inline= False)
        embed.add_field(name= "Aliases", value= f"{aliases}", inline= False)
        embed.timestamp = datetime.datetime.utcnow()
        
        await self.context.send(embed= embed)
