import re

import discord
from discord.ext import commands
from main import CTBot


class AutoResponse(commands.Cog):
    def __init__(self, bot: CTBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Checks if the message contains an AutoResponse trigger."""
        if not message.author.bot and message.channel:
            statements = self.bot.config["statements"]  # type: dict

            for item in statements:
                if item in str(message.content):
                    await message.channel.send(f"{statements.get(item)}")


def setup(bot):
    bot.add_cog(AutoResponse(bot))
