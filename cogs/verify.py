import random
import string
from random import *

import discord
from discord.ext import commands

from bot import CTBot


class Verify(commands.Cog):
    def __init__(self, bot: CTBot):
        self.bot = bot

    # noinspection PyMethodParameters
    async def on_member_join(self, ctx: commands.Context, member: discord.Member):
        # noinspection PyUnusedLocal
        key = "".join(
            [random.choice(strong.ascii_letters + string.digits) for n in range(32)]
        )
        await member.send(
            "Hello! Thank you for joining! This server is "
            "powered by CTBot. Please "
            "solve repeat this simple key "
            "(you can copy and paste) back to the bot to"
            "get the Verified role: " + key
        )
        while True:
            msg = self.bot.wait_for("message", check=check)
            if msg.guild is None:
                continue
            if str(msg) is key:
                await member.send("Thank you, you have been verified!")
            else:
                await member.send(
                    "Sorry, you have failed the CAPTCHA. "
                    "Please DM a Server Developer to grant "
                    "you the rank. If you are having issues, "
                    "please DM `ProgrammerPlays#8264.`"
                )
                return
            rolever = "Verified"
            try:
                await member.add_roles(discord.utils.get(ctx.guild.roles, name=rolever))
            except discord.HTTPException:
                await member.send(
                    "An error occurred, please contact "
                    "a developer or ProgrammerPlays#8264."
                )


def setup(bot: CTBot):
    bot.add_cog(Verify(bot))
