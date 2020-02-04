import discord
from discord.ext import commands
from discord.ext.commands import Greedy

from utils import utils


def has_required_permissions(**kwargs):
    """Permission and role check."""

    async def predicate(ctx):
        if all((perm, value) in list(ctx.author.guild_permissions) for perm, value in kwargs.items()):
            if kwargs:  # Make sure it's not empty because all() returns True if empty
                return True
        name = ctx.command.name
        if name.startswith('un'):
            name = name[2:]
        return any(role.id in ctx.bot.config['moderator'][name] for role in ctx.author.roles)

    return commands.check(predicate)


class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Mute a user.")
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.cooldown(5, 60, commands.BucketType.user)
    @commands.cooldown(10, 60, commands.BucketType.guild)
    @commands.guild_only()
    @has_required_permissions(manage_roles=True)
    @commands.bot_has_permissions(embed_links=True, manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        # support = discord.utils.get(ctx.guild.roles, name="Support")
        if member.top_role.position >= ctx.author.top_role.position:
            return await ctx.send("That member has a higher rank than you.")
        muted = discord.utils.get(member.guild.roles, name="Muted")
        await member.add_roles(muted)
        e = discord.Embed()
        e.set_author(name=f"{member} was muted", icon_url=member.avatar_url)
        await ctx.send(embed=e)

    @commands.command(description="Unmute a user.")
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.cooldown(5, 60, commands.BucketType.user)
    @commands.cooldown(10, 60, commands.BucketType.guild)
    @commands.guild_only()
    @has_required_permissions(manage_roles=True)
    @commands.bot_has_permissions(embed_links=True, manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        # support = discord.utils.get(ctx.guild.roles, name="Support")
        if member.top_role.position >= ctx.author.top_role.position:
            return await ctx.send("That member has a higher rank than you.")
        muted = discord.utils.get(member.guild.roles, name="Muted")
        await member.remove_roles(muted)
        e = discord.Embed()
        e.set_author(name=f"{member} was unmuted", icon_url=member.avatar_url)
        await ctx.send(embed=e)

    @commands.command(description="Kick a user from the server.")
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.cooldown(5, 60, commands.BucketType.user)
    @commands.cooldown(10, 60, commands.BucketType.guild)
    @commands.guild_only()
    @has_required_permissions(kick_members=True)
    @commands.bot_has_permissions(embed_links=True, kick_members=True)
    async def kick(self, ctx, members: Greedy[discord.Member], *, reason=None):
        """Kicks a user based on a mention"""
        # support = discord.utils.get(ctx.guild.roles, name="Support")
        if not reason:
            reason = f"Kicked by {ctx.author}"
        for member in members:
            if member.top_role.position >= ctx.author.top_role.position:
                await ctx.send("That member has a higher rank than you.")
                continue
            try:
                await member.send(f"You've been kicked from {ctx.guild} for {reason}")
            except discord.errors.Forbidden:
                pass
            await member.kick(reason=reason)
            e = discord.Embed()
            e.set_author(name=f"{member} was kicked", icon_url=member.avatar_url)
            await ctx.send(embed=e)

    @commands.command(description="Ban a user from the server.")
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.cooldown(5, 60, commands.BucketType.user)
    @commands.cooldown(10, 60, commands.BucketType.guild)
    @commands.guild_only()
    @has_required_permissions(ban_members=True)  # i swapped out the ban one cuz this one has a perm check as well
    @commands.bot_has_permissions(embed_links=True, ban_members=True)
    async def ban(self, ctx, locator: str, *, reason: str = None):
        # support = discord.utils.get(ctx.guild.roles, name="Support")
        member = await commands.MemberConverter().convert(ctx, locator)
        if not member:
            member = await commands.UserConverter().convert(ctx, locator)
        if not member:
            return await ctx.send("I can't find that member")
        if isinstance(member, discord.Member):
            if member.top_role.position >= ctx.author.top_role.position:
                return await ctx.send("That member has a higher rank than you.")
        try:
            inv = f'https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=0&scope=bot'
            e = discord.Embed(color=utils.theme_color(ctx))
            e.description = f"[in case you need my invite to DM me]({inv})."
            await member.send("Seems you were banned in the crafting table..\n"
                              "You can either use `ct!appeal your_appeal` to request an unban, "
                              "or fill out a form at https://forms.gle/dCLv2QZq5LHdyTuL8. Do note "
                              "that the command is more likely to get a response", embed=e)
        except discord.errors.Forbidden:
            pass
        await ctx.guild.ban(member, reason=reason)
        e = discord.Embed()
        e.set_author(name=f"{member} was banned", icon_url=member.avatar_url)
        await ctx.send(embed=e)

    @commands.command(description="Unban a user from the server.")
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.cooldown(10, 60, commands.BucketType.guild)
    @commands.guild_only()
    @has_required_permissions(ban_members=True)
    @commands.bot_has_permissions(embed_links=True, ban_members=True)
    async def unban(self, ctx, user: str, reason='unspecified'):
        # support = discord.utils.get(ctx.guild.roles, name="Support")
        banlist = await ctx.guild.bans()
        if not banlist:
            return await ctx.send("Banlist is empty")
        for ban in banlist:
            if str(ban[1]) == user.lstrip('@'):
                try:
                    await ctx.guild.unban(ban[1], reason=f"Unbanned by {ctx.author}: {reason}")
                    return await ctx.send(f"{user} was unbanned")
                except discord.errors.Forbidden:
                    await ctx.send("Action forbidden")
                except discord.errors.HTTPException:
                    await ctx.send("Unban failed")
        await ctx.send("User isn't banned")


def setup(bot):
    bot.add_cog(ModCommands(bot))
