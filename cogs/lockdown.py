# prevent users from sending messages throughout the server

import discord
from discord.ext import commands

from utils import checks


def has_required_permissions():
	""" Only allow Elon and/or the server owner """
	async def predicate(ctx):
		# if ctx.guild.id != 1234:  # replace with crafting table id
		#	await ctx.send("This can only be used in the crafting table!")
		if not ctx.author.id in checks.owner_ids:
			await ctx.send("Only Elon can use this")
			return False
		return True
	return commands.check(predicate)


def usage():
	e = discord.Embed()
	e.description = 'ct!lockdown\n`mass updates channel overwrites to deny everything perms to send`' \
					'\nct!unlock\n`undoes the actions of ct.lockdown`'
	return e


class Lockdown(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.overwrites = {}

	@commands.command(name='lockdown', usage=usage(), description='locks the server')
	@commands.cooldown(1, 5, commands.BucketType.user)
	@has_required_permissions()
	@commands.bot_has_permissions(administrator=True)
	async def lockdown(self, ctx):
		await ctx.send(f"Locking down the server..\nEstimated time: {len(ctx.guild.text_channels)}s")
		for channel in ctx.guild.text_channels:
			self.overwrites[channel] = channel.overwrites
			new_overwrites = {}
			for overwrite, perms in channel.overwrites.items():
				perms.update(send_messages=False)
				new_overwrites[overwrite] = perms
			if ctx.guild.default_role not in channel.overwrites:
				perms = discord.PermissionOverwrite()
				perms.update(send_messages=False)
				new_overwrites[ctx.guild.default_role] = perms
			await channel.edit(overwrites=new_overwrites)
		await ctx.send("Finished locking the server\nUse the unlock cmd to undo")

	@commands.command(name='unlock', usage=usage(), description='unlocks the server')
	@commands.cooldown(1, 5, commands.BucketType.user)
	@has_required_permissions()
	@commands.bot_has_permissions(administrator=True)
	async def unlock(self, ctx):
		await ctx.send(f"Unlocking the server..\nEstimated time: {len(ctx.guild.text_channels)}s")
		for channel, overwrites in self.overwrites.items():
			await channel.edit(overwrites=overwrites)
		await ctx.send("Finished unlocking the server")
		self.overwrites = {}


def setup(bot):
	bot.add_cog(Lockdown(bot))
