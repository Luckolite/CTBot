# dev only stuff

import os

import discord
from discord.ext import commands

from utils import checks


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        return checks.dev(ctx)

    @commands.command(description="Restarts the bot")
    async def restart(self, ctx):
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Restarting"))
        os.system("pm2 restart ctbot")
        await ctx.send("Restarting.. check my status for updates")

    @commands.command(description="Reloads cogs.")
    async def reload(self, ctx):
        await self.bot.reload()
        await ctx.send('Reloaded bot')


def setup(bot):
    bot.add_cog(Dev(bot))
