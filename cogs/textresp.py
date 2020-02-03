from discord.ext import commands


class TextResp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    def on_message(self, message):
        if message.author.bot:
            return
        message_str = message.cotnent  # don't wanna use str() on it cuz it removes custom emotes
        if "furnace" in message_str:
            await message.channel.send("crafting tables are obviously the superior block")
        elif "fit" in message_str:
            await message.channel.send("who dat")
        elif "@everyone" in message_str:
            await message.channel.send("no ping")
        else:
            return


def setup(bot):
    bot.add_cog(TextResp(bot))
