from random import randint
import asyncio

import discord
from discord.ext import commands

from bot import CTBot


class Coin(commands.Cog):
    def __init__(self, bot: CTBot):
        self.bot = bot

        self.lock = asyncio.Lock()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Randomly gives money to active members."""
        random_ct_int = randint(1, 250)
        if not message.author.bot and random_ct_int == 250:
            async with self.lock:
                user_id = str(message.author.id)

                if user_id not in self.bot.coin:
                    self.bot.coin[user_id] = 0
                self.bot.coin[user_id] += 1

                self.bot.save()

            await message.channel.send(
                f"{message.author.mention}, you just earned a crafting table!"
            )


def setup(bot: CTBot):
    bot.add_cog(Coin(bot))
