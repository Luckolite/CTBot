import re

import discord
from discord.ext import commands


class AutoResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Checks if the message contains an AutoResponse trigger."""
        if not message.author.bot and message.channel:
            statements = {
                "furnace": "crafting table is obviously the superior block",
                "fit": "who dat",
                "@everyone": "<:ping:623235635897171999>",
                "kek": "now thats a bruh moment",
            }

            for item in statements:
                if str(message.content).count(item) > 0:
                    await message.channel.send(statements[item])


def setup(bot):
    bot.add_cog(AutoResponse(bot))
