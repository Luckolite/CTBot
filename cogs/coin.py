import asyncio
import json

import discord
from discord.ext import commands

from utils import colors

from random import random
from random import randint

class Coin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.suggest_channel_id = 672135121469571092

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        with open('../data/coindb.json') as c:
            coindb = json.load(c)
        if coindb[message.author.id]:
            coindb[message.author.id] = 0
        randomctint = randint(1, 250)
        if randomctint == 250:
            coindb[message.author.id] += 1
        with open('../data/coindb.json') as d:
            json.dump(coindb, d, indent=2)


def setup(bot):
    bot.add_cog(Coin(bot))
