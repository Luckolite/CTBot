import datetime
import time
from datetime import timedelta

import discord
from discord.ext import commands

from bot import CTBot

start_time = time.time()


class Server(commands.Cog):
    def __init__(self, bot: CTBot):
        self.bot = bot

    @commands.command(
        description="Get various server statistics.", aliases=["server", "ping"]
    )
    async def uptime(self, ctx: commands.Context):
        current_time = time.time()
        bot_uptime_difference = int(round(current_time - start_time))
        bot_text = str(datetime.timedelta(seconds=bot_uptime_difference))
        with open("proc/uptime") as f:
            uptime_seconds = int(float(f.readline().split()[0]))
            uptime_string = str(timedelta(seconds=uptime_seconds))
        ping = ctx.bot.latency
        embed = discord.Embed(color=ctx.message.author.top_role.color)
        embed.add_field(name="Bot Uptime", value=bot_text)
        embed.add_field(name="Server Uptime", value=uptime_string)
        embed.add_field(name="Ping", value=ping)
        embed.set_footer(text="CTBot Uptime Statistics")
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Bot uptime: " + bot_text)


def setup(bot: CTBot):
    bot.add_cog(Server(bot))
