# dev only stuff
import os

import discord
from discord.ext import commands

from utils import checks, utils


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """Checks if the author can use a command from this cog."""
        return checks.dev(ctx)

    @commands.command(description="Restarts the bot.")
    async def restart(self, ctx):
        """Restarts the bot."""
        await self.bot.change_presence(
            status=discord.Status.dnd, activity=discord.Game(name="Restarting")
        )
        os.system("pm2 restart ctbot")
        await ctx.send("Restarting.. check my status for updates")

    @commands.command(description="Reloads cogs.")
    async def reload(self, ctx):
        """Reloads cogs."""
        await self.bot.reload()
        await ctx.send("Reloaded bot")

    @commands.command(description="Stops the bot.")
    async def stop(self, ctx: commands.Context):
        """Stops the bot."""
        await ctx.send("I'll be back 👍")
        os.system("pm2 stop ctbot")

    @commands.command(description="Performs git pull.")
    async def pull(self, ctx: commands.Context):
        """Performs `git pull` and reloads."""
        if self.bot.config["dev_manage"]:
            os.system("git pull")
            await self.bot.reload()
        else:
            return await ctx.send(
                "The bot is not under developer management. You may not run this command."
            )

    @commands.command(description="Tests logging.")
    async def log(self, ctx: commands.Context, level: str, title: str, *description: str):
        await ctx.bot.log(title, ' '.join(description), utils.LogLevel.__dict__[level.upper()])


def setup(bot):
    bot.add_cog(Dev(bot))
