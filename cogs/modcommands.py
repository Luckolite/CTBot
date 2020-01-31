from typing import *

import discord
from discord.ext import commands
from discord.ext.commands import Greedy


def has_required_permissions(**kwargs):
    """ Permission and/or role check """
    async def predicate(ctx):
        perms = ctx.author.guild_permissions
        if all(eval(f"{perms}.{perm}") == value for perm, value in kwargs.items()):
            if kwargs:  # Make sure it's not empty because all() returns True if empty
                return True
        config = {
            'mute': [],  # Role ids that can access
            'kick': [],
            'ban': []
        }
        return any(role.id in config[ctx.command.name] for role in ctx.author.roles)
    return commands.check(predicate)


class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mute")
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.cooldown(5, 60, commands.BucketType.user)
    @commands.cooldown(10, 60, commands.BucketType.guild)
    @commands.guild_only()
    @has_required_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(embed_links=True, manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        """mutes a user based on a mention"""
        muted = discord.utils.get(member.guild.roles, name="Muted")
        await member.add_roles(muted)
        e = discord.Embed()
        e.set_author(name=f"{member} was muted", icon_url=member.avatar_url)
        await ctx.send(embed=e)

    @commands.command(name="kick")
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.cooldown(5, 60, commands.BucketType.user)
    @commands.cooldown(10, 60, commands.BucketType.guild)
    @commands.guild_only()
    @has_required_permissions(kick_members=True)
    @commands.bot_has_permissions(embed_links=True, kick_members=True)
    async def kick(self, ctx, members: Greedy[discord.Member], *, reason):
        """Kicks a user based on a mention"""
        for member in members:
            await member.kick(reason=reason)
            e = discord.Embed()
            e.set_author(name=f"{member} was kicked", icon_url=member.avatar_url)
            await ctx.send(embed=e)
   
    @commands.command(name="ban")
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.cooldown(5, 60, commands.BucketType.user)
    @commands.cooldown(10, 60, commands.BucketType.guild)
    @commands.guild_only()
    @has_required_permissions(ban_members=True)  # i swapped out the ban one cuz this one has a perm check as well
    @commands.bot_has_permissions(embed_links=True, ban_members=True)
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
        if not member:
            return await ctx.send("I can't find that member")
        try:
            await member.send("Seems you were banned in the crafting table..\n"  # we want them to appeal with the bot
                              "you can use `ct!appeal your_appeal` to request an unban")
        except discord.errors.Forbidden:
            pass
        # await member.send(f"""you have been banned from {ctx.guild.name}.
        #                     fill out the forum to appeal for an unban.
        #                     https://forms.gle/dCLv2QZq5LHdyTuL8""")
        await ctx.guild.ban(member, reason)
        e = discord.Embed()
        e.set_author(name=f"{member} was banned", icon_url=member.avatar_url)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(ModCommands(bot))
