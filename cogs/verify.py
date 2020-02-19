from discord.ext import commands
import discord
import discord.utils
import random
from random import *
import string


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # noinspection PyMethodParameters
    async def on_member_join(self, ctx, member):
        # noinspection PyUnusedLocal
        key = "".join(
            [random.choice(strong.ascii_letters + string.digits) for n in xrange(32)]
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
                member.send("Thank you, you have been verified!")
            else:
                member.send(
                    "Sorry, you have failed the CAPTCHA. "
                    "Please DM a Server Developer to grant "
                    "you the rank. If you are having issues, "
                    "please DM `ProgrammerPlays#8264.`"
                )
                return
            rolever = "Verified"
            try:
                await user.add_roles(discord.utils.get(ctx.guild.roles, name=rolever))
            except Exception as e:
                await member.send(
                    "An error occured, please contact "
                    "a developer or ProgramerPlays#8264."
                )


def setup(bot):
    bot.add_cog(Verify(bot))
