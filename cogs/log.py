import discord
from discord.ext import commands


class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Show log")
    async def logs(self, ctx):
        with open("log.txt", "r") as c:
            await ctx.send(str(c))

    @commands.command(description="Clear log")
    async def clog(self):
        logf = open("../log.txt", "w")
        logb = open("../backup.txt", "w")
        logb.write(str(logf))
        logf.write("")
        logb.close()
        logf.close()


def setup(bot):
    bot.add_cog(Log(bot))
