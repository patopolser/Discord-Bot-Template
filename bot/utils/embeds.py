from datetime import datetime

import discord

from bot import (
    VERSION,
    AVATAR,
)

class Embeds:
    def embed(member, description: str):
        embed = discord.Embed(
            description = description,
            color = 0x2b2d31,
        )
        embed.set_author(name = member, icon_url = member.display_avatar)
        embed.timestamp = datetime.utcnow()

        return embed

    def error_embeds(description: str, title: str = "Error"):
        embed = discord.Embed(
            title = title,
            description = description,
            color = discord.Colour.red()
        )
        embed.set_footer(text = f"v{VERSION}", icon_url= AVATAR)
        embed.timestamp = datetime.utcnow()

        return embed