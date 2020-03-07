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
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # noinspection PyUnusedLocal
        key = "".join(
            [choice(string.ascii_letters + string.digits) for n in range(32)]
        )
        await member.send(
            "Hello! Thank you for joining! This server is "
            "powered by CTBot. Please respond "
            "by repeating this simple key "
            "(you can copy and paste) back to the bot to"
            "get the Verified role: " + key
        )

        def check(m):
            return m.author == member

        while True:
            msg = await self.bot.wait_for("message", check=check)
            await self.bot.log("VERIFY", f"Received message {str(msg.content)}")

            if str(msg.content) == key:
                await member.send("Thank you, you have been verified!")
            else:
                await member.send(
                    "Sorry, you have failed the CAPTCHA. "
                    "Please DM a Server Developer to grant "
                    "you the rank. If you are having issues, "
                    "please DM `ProgrammerPlays#8264.`"
                )
                return

            try:
                await member.add_roles(
                    discord.utils.get(member.guild.roles, name="Verified")
                )
            except discord.HTTPException or AttributeError:
                await member.send(
                    "An error occurred, please contact "
                    "a developer or ProgrammerPlays#8264."
                )


def setup(bot: CTBot):
    bot.add_cog(Verify(bot))
