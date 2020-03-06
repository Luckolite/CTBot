from pathlib import Path
import re

import discord
from discord.ext import commands

from bot import CTBot


class Search(commands.Cog):

    other_words = ['dox', 'pastebin']

    def __init__(self, bot: CTBot):
        self.bot = bot

        read = lambda x: str(x.read_text()).lower().strip().split('\n')

        pathln = Path("./lastnames.txt")
        if pathln.is_file():
            ln = read(pathln)
        else:
            raise ValueError("We are missing the lastnames file.")

        pathfn = Path("./firstnames.txt")
        if pathfn.is_file():
            fn = [x.split(",", 1)[0] for x in read(pathfn)]
        else:
            raise ValueError("We are missing the firstnames file.")

        pathcn = Path("./cities.txt")
        if pathcn.is_file():
            cn = read(pathcn)
        else:
            raise ValueError("We are missing the cities file.")

        search_terms = filter(lambda x: x, map(str.strip, fn + ln + cn + self.other_words))
        self.regex = re.compile(
            f"\\b({'|'.join(search_terms)})\\b",
            flags=re.IGNORECASE
        )

    @commands.command(description="Find TOS-breaking content in the channel.")
    async def search(self, ctx: commands.Context, guild_id: int):
        await ctx.send("starting the `TOS BREAKING SEARCH`")
        delmsg = None
        delcnt = 0

        guild = self.bot.get_guild(guild_id)
        channels = guild.text_channels

        for channel in channels:
            messages = channel.history(limit=None)

            async for message in messages:
                msg = str(message.content)

                if self.regex.search(msg) is not None:
                    delcnt += 1
                    delmsg = True

                    await message.delete()

        if delmsg:
            embed = discord.Embed(
                title="Removed Messages (TOS Safety)",
                description="Messages were removed for" "breaking the TOS",
                color=0xFF2103,
            )
            embed.add_field(name="Count:", value=str(delcnt), inline=False)
            embed.add_field(name="Issuer", value=str(ctx.author.name), inline=False)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("No content in violation of the TOS was found.")


def setup(bot: CTBot):
    bot.add_cog(Search(bot))
