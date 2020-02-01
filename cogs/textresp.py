import asyncio
import json

import discord
from discord.ext import commands

from utils import colors

from random import random
from random import randint

class TextResp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    def on_message(self, message):
        if message.author.bot:
            return
        messagestr = str(message.content)
        if "furnace" in messagestr:
            message.channel.send("crafting tables are obviously the superior block")
        elif "fit" in messagestr:
            message.channel.send("who dat")
        elif "@everyone" in messagestr:
            message.channel.send("no ping")
        else:
            return


def setup(bot):
    bot.add_cog(TextResp(bot))
