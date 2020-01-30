# dev only stuff

import os

from discord.ext import commands

from utils import checks


class Dev(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='restart', description='completely restart the bot')
	@commands.check(checks.dev)
	async def restart(self, ctx):
		os.system('pm2 restart ctbot')
		await ctx.send("Restarting.. check my status for updates")


def setup(bot):
	bot.add_cog(Dev(bot))
