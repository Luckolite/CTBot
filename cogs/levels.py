from random import randint

from discord.ext import commands


class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        randomlint = randint(1, 5)
        if not message.author.bot and randomlint == 5:
            user_id = str(message.author.id)
            if user_id not in self.bot.xpdb:
                self.bot.xpdb[user_id] = 0
            self.bot.xpdb[user_id] += 1

            if user_id not in self.bot.ldb:
                self.bot.ldb[user_id] = 0

            lxp = (self.bot.ldb[user_id] + 1) * (
                100 + (2 ** (self.bot.ldb[user_id] + 1))
            )
            if self.bot.xpdb[user.id] >= lxp:
                self.bot.ldb[user_id] += 1
                await message.channel.send(
                    message.author.id
                    + ", you leveled up to "
                    + str(self.bot.ldb[user_id])
                )
            self.bot.save_ldb()
            self.bot.save_xpdb()


def setup(bot):
    bot.add_cog(Levels(bot))
