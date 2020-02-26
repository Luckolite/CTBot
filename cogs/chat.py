import sys

import cleverbotfree.cbfree
import discord
from discord.ext import commands

from bot import CTBot


class Chat(commands.Cog):
    def __init__(self, bot: CTBot):
        self.bot = bot

        self.cb = cleverbotfree.cbfree.Cleverbot()

    @commands.command(description="Enter chat")
    async def chat(self, ctx: commands.Context):
        try:
            self.cb.browser.get(self.cb.url)
        except:
            self.cb.browser.close()
            sys.exit()
        while True:
            try:
                self.cb.get_form()
            except:
                sys.exit()

            def check(m: discord.Message):
                return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

            msg = await self.bot.wait_for("message", check=check)
            input_text: object = msg.content
            user_input = str(input_text)
            if user_input == "quit":
                break
            cb.send_input(user_input)
            resp = cb.get_response()
            await ctx.send(str(resp))
        cb.browser.close()


def setup(bot: CTBot):
    bot.add_cog(Chat(bot))
