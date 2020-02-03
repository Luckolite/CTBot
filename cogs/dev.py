# dev only stuff

import os

import discord
from discord.ext import commands

from utils import checks


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='restart', description='completely restart the bot')
    @commands.check(checks.dev)
    async def restart(self, ctx):
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name='Restarting'))
        os.system('pm2 restart ctbot')
        await ctx.send("Restarting.. check my status for updates")


def setup(bot):
    bot.add_cog(Dev(bot))
