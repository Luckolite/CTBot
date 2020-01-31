import asyncio
import json

import discord
from discord.ext import commands
from discord.utils import get

from utils import colors

from random import random
from random import randint

class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.suggest_channel_id = 672135121469571092

    @bot.command
    async def kick(ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Support")
        if role in ctx.author.roles:
            await bot.kick(member)
    
    @bot.command
    async def mute(ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Support")
        if role in ctx.author.roles:
            muted = discord.utils.get(member.guild.roles, name="Muted")
            await bot.add_roles(member, muted)
            await ctx.send("User muted")
            

def setup(bot):
    bot.add_cog(ModCommands(bot))
