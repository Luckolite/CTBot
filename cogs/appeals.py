
from os import path
import json
import asyncio
from time import time

from discord.ext import commands
import discord

from utils import colors


class Appeals(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.path = './data/appeal_blacklist.json'
		self.blacklist = {
			'1234': {  # example
				'cooldown': None,  # future time object
				'banned': False  # no longer able to submit appeals
			}
		}
		if path.isfile(self.path):
			with open(self.path, 'r') as f:
				self.blacklist = json.load(f)  # type: dict
		self.ct_id = 614889263183560840  # server id
		self.channel_id = 672498231103455233  # dedicated appeals channel

	def save_data(self):
		with open(self.path, 'w+') as f:
			json.dump(self.blacklist, f)

	@commands.command(name='appeal', description='request a ban appeal')
	@commands.cooldown(2, 30, commands.BucketType.user)
	@commands.cooldown(1, 1)
	async def appeal(self, ctx, *, appeal):
		""" request a ban appeal in the crafting table """
		user_id = str(ctx.author.id)
		if user_id in self.blacklist:
			if self.blacklist[user_id]['banned']:
				return await ctx.send(f"You are banned from submitting appeals")
			if self.blacklist[user_id]['cooldown']:
				if time() < self.blacklist[user_id]['cooldown']:
					return await ctx.send("You're on a 2 day cooldown due to your appeal being denied")

		channel = self.bot.get_channel(self.channel_id)
		try:
			ban_entry = await channel.guild.fetch_ban(ctx.author)
		except discord.errors.NotFound:
			return await ctx.send("You're not banned :/")

		e = discord.Embed(color=colors.theme())
		e.description = "Appeals need to contain the reason for your ban, and your reason " \
		                "for being unbanned. Lack of either, or abuse of this command results " \
		                "in being blocked from using it permanently"
		for text_group in [appeal[i:i + 1000] for i in range(0, len(appeal), 1000)]:
			e.add_field(name='◈ Your Appeal', value=text_group, inline=False)
		e.set_footer(text='React to accept/deny')
		msg = await ctx.send(embed=e)
		await msg.add_reaction('👍')
		await msg.add_reaction('👎')

		def pred(r, u):
			""" assure the conditions of the reaction is in the right location """
			return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id

		try:
			reaction, user = await self.bot.wait_for('reaction_add', check=pred, timeout=360)
		except asyncio.TimeoutError:
			return await msg.edit(content='This menu has expired', embed=e)
		if str(reaction.emoji) == '👍':
			e = discord.Embed(color=ctx.author.color)
			e.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
			if isinstance(ctx.guild, discord.Guild):
				e.set_thumbnail(url=ctx.guild.icon_url)
			e.description = appeal
			e.add_field(name='◈ Logged Ban Reason', value=str(ban_entry.reason))
			e.set_footer(text=str(ctx.author.id))
			appeal = await channel.send(embed=e)
			await appeal.add_reaction('👍')
			await appeal.add_reaction('👎')
			await appeal.add_reaction('🛑')
			await ctx.send('Sent your appeal request to CT')
		elif str(reaction.emoji) == '👎':
			await ctx.send("Alright, feel free to resubmit with the correct parameters")
		else:
			await msg.clear_reaction(reaction.emoji)

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.channel_id == self.channel_id:
			channel = self.bot.get_channel(payload.channel_id)
			msg = await channel.fetch_message(payload.message_id)
			user = channel.guild.get_member(payload.user_id)
			if user.bot:
				return
			if not user.guild_permissions.administrator:
				return await msg.remove_reaction(payload.emoji, user)
			target_id = msg.embeds[0].footer.text
			target = self.bot.get_user(int(target_id))
			emoji = str(payload.emoji)
			if emoji == '👍':
				await channel.guild.unban(target, reason=f"Appeal by {user}")
				await msg.edit(content=f"Unbanned by {user}", embed=msg.embeds[0])
				try:
					await target.send("Your appeal request was accepted")
				except discord.errors.Forbidden:
					pass
			elif emoji == '👎':
				await msg.edit(content=f"Appeal rejected by {user}", embed=msg.embeds[0])
				await msg.clear_reactions()
				self.blacklist[target_id] = {
					'cooldown': time() + 60*60*24*2,
					'banned': False
				}
				self.save_data()
				try:
					await target.send("Your ban appeal was denied, you can retry in 2 days")
				except discord.errors.Forbidden:
					pass
			elif emoji == '🛑':
				await msg.edit(content=f"Banned from appeals by {user}", embed=msg.embeds[0])
				await msg.clear_reactions()
				self.blacklist[target_id] = {
					'cooldown': None,
					'banned': True
				}
				self.save_data()
				try:
					await target.send("Your ban appeal was rejected an you've been banned from ban appeals")
				except discord.errors.Forbidden:
					pass
			else:
				await msg.clear_reaction(payload.emoji)


def setup(bot):
	bot.add_cog(Appeals(bot))
