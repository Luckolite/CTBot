# dev only stuff

import os

import discord
from discord.ext import commands

from utils import checks


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """Checks if the author can use a command from this cog."""
        return checks.dev(ctx)

    @commands.command(description="Restarts the bot.", hidden=True)
    async def restart(self, ctx):
        """Restarts the bot."""
        await self.bot.change_presence(
            status=discord.Status.dnd, activity=discord.Game(name="Restarting")
        )
        os.system("pm2 restart ctbot")
        await ctx.send("Restarting.. check my status for updates")

    @commands.command(description="Reloads cogs.", hidden=True)
    async def reload(self, ctx):
        """Reloads cogs."""
        await self.bot.reload()
        await ctx.send("Reloaded bot")

    @commands.check(checks.owner)
    @commands.command(description="Stops the bot.", hidden=True)
    async def _stop(self, ctx: commands.Context):
        """Stops the bot."""
        await ctx.send("I'll be back 👍")
        os.system("pm2 stop ctbot")


def setup(bot):
    bot.add_cog(Dev(bot))
