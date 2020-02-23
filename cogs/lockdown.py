import discord
from discord.ext import commands

from bot import CTBot
from utils import checks


def usage():
    e = discord.Embed()
    e.description = (
        "`ct!lockdown`\nMass updates channel overrides to deny everyone perms to send.\n"
        "`ct!unlock`\nUndoes the actions of ct!lockdown."
    )
    return e


class Lockdown(commands.Cog):
    def __init__(self, bot: CTBot):
        self.bot = bot
        self.overwrites = {}

    async def cog_check(self, ctx: commands.Context):
        """Checks if the author can use commands from this cog in the server, where the command was sent."""
        # if ctx.guild.id != 1234:  # replace with crafting table id
        #     await ctx.send("This can only be used in the crafting table!")
        if not checks.owner(ctx):
            await ctx.send("Only Elon can use this")
            return False
        return True

    @commands.command(
        description="Mass updates channel overrides to deny everyone permissions to send messages."
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.bot_has_permissions(administrator=True)
    async def lockdown(self, ctx: commands.Context):
        """Mass updates channel overrides to deny everyone permissions to send messages."""
        await ctx.send(
            f"Locking down the server..\nEstimated time: {len(ctx.guild.text_channels)}s"
        )
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

    @commands.command(description="Un-does the actions of ct!lockdown.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.bot_has_permissions(administrator=True)
    async def unlock(self, ctx: commands.Context):
        """Un-does the actions of ct!lockdown."""
        await ctx.send(
            f"Unlocking the server..\nEstimated time: {len(ctx.guild.text_channels)}s"
        )
        for channel, overwrites in self.overwrites.items():
            await channel.edit(overwrites=overwrites)
        await ctx.send("Finished unlocking the server")
        self.overwrites = {}


def setup(bot: CTBot):
    bot.add_cog(Lockdown(bot))
