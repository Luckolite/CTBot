import asyncio
import json

import discord
from discord.ext import commands

from utils import colors

from random import random
from random import randint

import datetime
import time
from datetime import timedelta

start_time = time.time()

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='uptime', description='Get various server statistics.', aliases='server, ping')
    async def uptime(self, ctx):
        current_time = time.time()
        botuptimedifference = int(round(current_time - start_time))
        bottext = str(datetime.timdelta(seconds=difference))
        with open('proc/uptime', 'r') as f:
            uptime_seconds = int(float(f.readline().split()[0]))
            uptime_string = str(timedelta(seconds = uptime_seconds))
        ping = bot.latency
        embed = discord.Embed(color=ctx.message.author.top_role.color)
        embed.add_field(name="Bot Uptime", value=bottext)
        embed.add_field(name="Server Uptime", value=uptime_string)
        embed.add_field(name="Ping", value=ping)
        embed.set_footer(text="CTBot Uptime Statistics")
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Bot uptime: " + bottext)

def setup(bot):
    bot.add_cog(Server(bot))
