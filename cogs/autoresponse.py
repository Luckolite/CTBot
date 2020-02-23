import discord
from discord.ext import commands


class AutoResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Checks if the message contains an AutoResponse trigger."""
        if not message.author.bot:
            words = message.content.lower().split()
            statements = {
                "furnace": "crafting table is obviously the superior block",
                "fit": "who dat",
                "@everyone": "<:ping:623235635897171999>",
            }

            for item in statements:
                if item in words:
                    await message.channel.send(statements[item])


def setup(bot):
    bot.add_cog(AutoResponse(bot))
