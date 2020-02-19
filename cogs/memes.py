from discord.ext import commands
import praw
import random
from random import randint


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Get a meme")
    async def meme(self, ctx):
        sub = randint(0, 4)
        if sub is 0:
            gs = 'memes'
        elif sub is 1:
            gs = 'dankmemes'
        elif sub is 2:
            gs = 'deepfriedmemes'
        elif sub is 3:
            gs = 'specialsnowflake'
        elif sub is 4:
            gs = 'imtoriginals'
        r = praw.Reddit(user_agent='example')
        
        rs = r.get_subreddit(gs)
        posts = rs.get_random_submission()
        ctx.send(posts.url)


def setup(bot):
    bot.add_cog(Memes(bot))
