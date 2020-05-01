from discord.ext import commands
import discord
from discord import Embed
from main import CTBot


class VC_things(commands.Cog):
    def __init__(self, bot: CTBot):
        self.bot = bot

    def get_nomic_role(self, guild: discord.Guild):
        for role in guild.roles:
            if role.name == "nomic":
                return role
        guild.create_role(
            reason="NOMIC AUTO ROLE-SETUP!",
            name="nomic",
            permissions=discord.PermissionOverwrite({}),
        )

    @commands.Cog.listener(name="on_voice_state_update")
    async def nomic(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        print(f"{member} || {before} || {after}")
        if after.channel is None:
            guild = member.guild  # type: discord.Guild


def setup(bot):
    bot.add_cog(VC_things(bot))
