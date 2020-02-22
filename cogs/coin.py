from random import randint

from discord.ext import commands


class Coin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """Randomly gives money to active members."""
        random_ct_int = randint(1, 250)
        if not message.author.bot and random_ct_int == 250:
            user_id = str(message.author.id)

            if user_id not in self.bot.coin:
                self.bot.coin[user_id] = 0
            self.bot.coin[user_id] += 1

            await message.channel.send(
                f"{message.author.id}, you just earned a crafting table!"
            )
            self.bot.save()


def setup(bot):
    bot.add_cog(Coin(bot))
