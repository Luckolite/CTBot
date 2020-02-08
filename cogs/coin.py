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

            if user_id not in self.bot.coindb:
                self.bot.coindb[user_id] = 0
            self.bot.coindb[user_id] += 1

            await message.channel.send(message.author.id + ", you just earned a crafting table!")
            self.bot.save_coindb()


def setup(bot):
    bot.add_cog(Coin(bot))
