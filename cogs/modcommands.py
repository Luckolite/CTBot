from typing import *

import discord
from discord.ext import commands
from discord.ext.commands import Greedy


def has_required_permissions():
    """ Permission and/or role check """
    async def predicate(ctx):
        if ctx.author.guild_permissions.administrator:
            return True
        config = {
            'kick': [],  # Role ids that can access
            'ban': []
        }
        return any(role.id in config[ctx.command.name] for role in ctx.author.roles)
    return commands.check(predicate)

def ban_members(): # ill remove later when "has_required_permisions" has roles setup in it.
    """Quick ban members check"""
    async def predicate(ctx):
        member = ctx.guild.get_member(ctx.author.id)
        return member.permissions_in(ctx.channel).ban_members:        
    return commands.check(predicate)

class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick")
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.cooldown(5, 60, commands.BucketType.user)
    @commands.cooldown(10, 60, commands.BucketType.guild)
    @commands.guild_only()
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, members: Greedy[discord.Member], *, reason):
        """Kicks a user based on a mention"""
        for member in members:
            await member.kick(reason=reason)
    
    @commands.command(name = "mute")
    async def mute(self, ctx, member: discord.Member):
        """mutes a user based on a mention"""
        role = discord.utils.get(ctx.guild.roles, name = "Support")
        if role in ctx.author.roles:
            muted = discord.utils.get(member.guild.roles, name = "Muted")
            await self.bot.add_roles(member, muted)
            await ctx.send("User muted")
   
    @commands.command(name="ban")
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @ban_members()
    async def ban(self, ctx, locator: str, *, reason: str = None):
        """Bans a user from the guild 
           locator can be the following message formats:
                Mention      - @Persons name
                ID           - 1234568765473
                name#discrim - Person12#1234
           Usage:
                ban [locator] {OPTIONAL: reason can be multiple words}
                ban 2347832428 He was disrespecting staff
                ban idk#4567 
        """
        member = await commands.UserConverter().convert(ctx, locator)
        await user.send(f"""you have been banned from {ctx.guild.name}.
                            fill out the forum to appeal for an unban.
                            https://forms.gle/dCLv2QZq5LHdyTuL8""")
        await ctx.guild.ban(member, reason)
        await ctx.send(f"banned {member}.")
            

def setup(bot):
    bot.add_cog(ModCommands(bot))
