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

    @commands.command(name = "kick")
    async def kick(self, ctx, member: discord.Member):
        """Kicks a user based on a mention"""
        role = discord.utils.get(ctx.guild.roles, name = "Support")
        if role in ctx.author.roles:
            await self.bot.kick(member)
    
    @commands.command(name = "mute")
    async def mute(self, ctx, member: discord.Member):
        """mutes a user based on a mention"""
        role = discord.utils.get(ctx.guild.roles, name = "Support")
        if role in ctx.author.roles:
            muted = discord.utils.get(member.guild.roles, name = "Muted")
            await self.bot.add_roles(member, muted)
            await ctx.send("User muted")
   
    @commands.command(name = "ban")
    async def ban(self, ctx, locator: str = None, *, reason: str = None) 
        """Bans a user from the guild
           locator can be the following message types:
                Mention      - @Persons name
                ID           - 1234568765473
                name#discrim - Person12#1234
           Usage:
                ban [locator] {OPTIONAL: reason can be multiple words}
                ban 2347832428 He was disrespecting staff
                ban idk#4567 
        """
                
        try:
            user = await commands.UserConverter().convert(ctx, locator)
            # send a message to the user explaining they have been banned and how to get unbanned
            await user.send(f"""Hi you have been banned from {ctx.guild.name}.
                                if you would like to come back. please fill out this forum.
                                https://forms.gle/dCLv2QZq5LHdyTuL8""")
            # ban the user from the guild. NOTE THIS IS SET TO NOT DELETE MESSAGES. 
            # REMOVE "delete_messages_days = 0" OR CHANGE VALUE TO DELETE MESSAGES!
            await ctx.guild.ban(user, reason, delete_message_days = 0)
            await ctx.send(f"the ban hammer has spoken:\n\t{user} has been banned.")

        # if the bot cannot find the user tell the person in chat.
        except commands.errors.BadArgument:
            await ctx.send(f"The user you where looking for {locator} could not be found.")
            

def setup(bot):
    bot.add_cog(ModCommands(bot))
