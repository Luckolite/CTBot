import random
from random import randrange

import praw
from discord.ext import commands

from bot import CTBot


class Memes(commands.Cog):
    def __init__(self, bot: CTBot):
        self.bot = bot

    @commands.command(description="Get a meme")
    async def meme(self, ctx: commands.Context):
        try:
            gs = ("memes", "dankmemes", "deepfriedmemes", "specialsnowflake", "imtoriginals")[randrange(5)]
            r = praw.Reddit(
                user_agent="Firefox 73.0 on Ubuntu Linux",
                client_id="aIm3Qc5zFyMljQ",
                client_secret="yupA7e-s8BOB9HDytRRwNhJDLE0",
            )

            rs = r.subreddit(gs)
            posts = rs.hot()
            post = random.choice(posts)
            await ctx.send(post.url)
        except Exception as e:
            print(str(e))


def setup(bot: CTBot):
    bot.add_cog(Memes(bot))
