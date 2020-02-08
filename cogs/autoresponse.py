from discord.ext import commands


class AutoResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    def on_message(self, message):
        if not message.author.bot:
            words = message.content.split()
            if "furnace" in words:
                await message.channel.send("crafting table is obviously the superior block")
            elif "fit" in words:
                await message.channel.send("who dat")
            elif "@everyone" in message.content:
                await message.channel.send("<:ping:623235635897171999>")


def setup(bot):
    bot.add_cog(AutoResponse(bot))
