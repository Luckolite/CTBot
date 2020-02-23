from os import path

import discord
from discord.ext import commands

# noinspection SpellCheckingInspection,PyUnusedLocal
from bot import CTBot


class Search(commands.Cog):
    def __init__(self, bot: CTBot):
        self.bot = bot

        if path.isfile("./lastnames.txt"):
            dataln = open("./lastnames.txt")
            self.ln = dataln.read()
            dataln.close()
        else:
            print("We are missing the lastnames file.")
            exit()

        if path.isfile("./firstnames.txt"):
            datafn = open("./firstnames.txt")
            self.fn = datafn.read()
            datafn.close()
        else:
            print("We are missing the firstnames file.")
            exit()

        if path.isfile("./cities.txt"):
            datacn = open("./cities.txt")
            self.cn = datacn.read()
            datacn.close()
        else:
            print("We are missing the cities file.")
            exit()

    @commands.command(description="Find TOS-breaking content in the channel.")
    async def search(self, ctx: commands.Context, guild_id: int):
        await ctx.send("starting the `TOS BREAKING SEARCH`")
        delmsg = None
        delcnt = 0

        lna = str(self.ln).split("\n")
        fna = str(self.fn).split("\n")
        cna = str(self.cn).split("\n")

        for item in lna:
            item.strip()
            item = item.split(",", 1)[0]
            item.lower()

        for item in fna:
            item.strip()
            item.lower()

        for item in cna:
            item.strip()
            item.lower()

        guild = self.bot.get_guild(guild_id)
        channels = guild.text_channels

        for channel in channels:
            messages = channel.history(limit=None)

            async for message in messages:
                msg = str(message.content)

                for lname in lna:
                    if msg.count(lname) > 0:
                        await ctx.send(f"Message was deleted!\n{msg}")
                        delcnt += 1
                        await message.delete()
                        delmsg = True
                        break

                for cname in cna:
                    if delmsg:
                        break
                    if msg.count(cname) > 0:
                        await ctx.send(f"Message was deleted!\n{msg}")
                        delcnt += 1
                        await message.delete()
                        delmsg = True
                        break

                for fname in fna:
                    if delmsg:
                        break
                    if msg.count(fname) > 0:
                        await ctx.send(f"Message was deleted!\n{msg}")
                        delcnt += 1
                        await message.delete()
                        delmsg = True
                        break

                if msg.count("pastebin") > 0 or msg.count("dox") > 0:
                    if delmsg:
                        break
                    await ctx.send(f"Message was deleted!\n{msg}")
                    delcnt += 1
                    await message.delete()
                    delmsg = True
                    break

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
