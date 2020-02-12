from random import randint

from discord.ext import commands


class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        rand = randint(1, 5)
        if not message.author.bot and rand == 5:
            user_id = str(message.author.id)
            if user_id not in self.bot.levels_xp_db:
                self.bot.levels_xp_db[user_id] = 0
            self.bot.levels_xp_db[user_id] += 1

            if user_id not in self.bot.levels_db:
                self.bot.levels_db[user_id] = 0

            if self.bot.levels_xp_db[user_id] >= (self.bot.levels_db[user_id] + 1) * (
                    100 + (2 ** (self.bot.levels_db[user_id] + 1))
            ):
                self.bot.levels_db[user_id] += 1
                await message.channel.send(
                    f"{message.author.mention}, you leveled up to {self.bot.levels_db[user_id]}!"
                )
            self.bot.save()


def setup(bot):
    bot.add_cog(Levels(bot))
