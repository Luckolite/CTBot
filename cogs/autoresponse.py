import re

from discord.ext import commands


class AutoResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """Checks if the message contains an AutoResponse trigger."""
        if not message.author.bot:
            statements = {
                "furnace": "crafting table is obviously the superior block",
                "fit": "who dat",
                "@everyone": "<:ping:623235635897171999>",
            }

            for item in statements:
                if re.search(f"\b{item}\b", message.content, flags=re.IGNORECASE) is not None:
                    await message.channel.send(statements[item])


def setup(bot):
    bot.add_cog(AutoResponse(bot))
