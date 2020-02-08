from discord.ext import commands  # imports


class AutoResponse(commands.Cog):  # the class
    def __init__(self, bot):  # go look at appeals for more advanced definitions.
        self.bot = bot

    @commands.Cog.listener()  # listener
    async def on_message(self, message):  # on message
        if not message.author.bot:  # if the message author is not a bot
            words = message.content.lower().split()  # gets the words in the message.
            statements = {  # the statements in json format
                "furnace": "crafting table is obviously the superior block",
                "fit": "who dat",
                "@everyone": "<:ping:623235635897171999>"
            }

            for item in statements:  # self explanetory
                if item in words:  # self explanetory
                    await message.channel.send(statements[item])  # easy to read


def setup(bot):
    bot.add_cog(AutoResponse(bot))
