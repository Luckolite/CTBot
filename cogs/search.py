from os import path

import discord
from discord.ext import commands


# noinspection SpellCheckingInspection,PyUnusedLocal
class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if path.isfile('lastnames.txt'):
            dataln = open("lastnames.txt", "r")
            self.ln = dataln.read()
            dataln.close()
        else:
            print("We are missing the lastnames file.")
            exit()

        if path.isfile('firstnames.txt'):
            datafn = open("firstnames.txt", "r")
            self.fn = datafn.read()
            datafn.close()
        else:
            print("We are missing the firstnames file.")
            exit()

        if path.isfile('cities.txt'):
            datacn = open("cities.txt", "r")
            self.cn = datacn.read()
            datacn.close()
        else:
            print("We are missing the cities file.")
            exit()

    @commands.command(description="Find TOS-breaking content in the channel.")
    async def search(self, ctx):

        print("Initiated")

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

        channels = discord.utils.get(ctx.guild.channels())

        for channel in channels:
            messages = await channel.history(limit=None)

            for message in messages:
                msg = str(message.content)

                print("Began a message tract")
                print("This will repeat")

                for lname in lna:
                    if lname in msg:
                        await ctx.send("Message was deleted!")
                        delcnt += 1
                        await message.delete()
                        delmsg = True
                        continue

                for cname in cna:
                    if delmsg:
                        continue
                    if cname in msg:
                        await ctx.send("Message was deleted!")
                        delcnt += 1
                        await message.delete()
                        delmsg = True
                        continue

                for fname in fna:
                    if delmsg:
                        continue
                    if fname in msg:
                        await ctx.send("Message was deleted!")
                        delcnt += 1
                        await message.delete()
                        delmsg = True
                        continue

                if "pastebin.com" in msg or "doxbin.org" in msg:
                    if delmsg:
                        continue
                    await ctx.send("Message was deleted!")
                    delcnt += 1
                    await message.delete()
                    delmsg = True
                    continue


        if delmsg:
            embed = discord.Embed(title="Removed Messages (TOS Safety)",
                                  description="Messages were removed for"
                                              "breaking the TOS",
                                  color=0xff2103)
            embed.add_field(name="Count:",
                            value=str(delcnt),
                            inline=False)
            embed.add_field(name="Issuer",
                            value=str(ctx.author.name),
                            inline=False)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed)
        else:
            ctx.send("No content in violation of the TOS was found.")


def setup(bot):
    bot.add_cog(Search(bot))
