import discord
import asyncio

from discord.ext import commands
from discord.ui import View
from discord.interactions import Interaction

from .embeds import Embeds

async def get_response(
    bot: commands.Bot, 
    ctx: commands.Context, 
    message: discord.Message, 
    interaction_type: str, 
    timeout: int
):
    try:
        interaction = await bot.wait_for(
            interaction_type, 
            check= lambda m: m.user == ctx.author and m.channel == ctx.channel if isinstance(m, Interaction) else m.author == ctx.author and m.channel == ctx.channel, 
            timeout= timeout
        )
        
        if (isinstance(interaction, Interaction)):  
            await interaction.response.defer()

        return interaction

    except asyncio.TimeoutError:
        await message.edit(embed= Embeds.embeds(ctx.author, "Timed out!"), view= View())
        return

async def get_response_no_ctx(
    bot: commands.Bot, 
    author: discord.Member, 
    channel: discord.TextChannel, 
    message: discord.Message, 
    interaction_type: str, 
    timeout: int
):
    try:
        interaction = await bot.wait_for(
            interaction_type, 
            check= lambda m: m.user == author and m.channel == channel if isinstance(m, Interaction) else m.author == author and m.channel == channel, 
            timeout= timeout
        )
        
        if (isinstance(interaction, Interaction)):  
            await interaction.response.defer()

        return interaction

    except asyncio.TimeoutError:
        await message.edit(embed= Embeds.embeds(author, "Timed out!"), view= View())
        return
