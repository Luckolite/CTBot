from os import path

import discord
from discord.ext import commands


# noinspection SpellCheckingInspection,PyUnusedLocal
class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if path.isfile('./lastnames.txt'):
            dataln = open("./lastnames.txt", "r")
            self.ln = dataln.read()
            dataln.close()
        else:
            print("We are missing the lastnames file.")
            exit()

        if path.isfile('./firstnames.txt'):
            datafn = open("./firstnames.txt", "r")
            self.fn = datafn.read()
            datafn.close()
        else:
            print("We are missing the firstnames file.")
            exit()

        if path.isfile('./cities.txt'):
            datacn = open("./cities.txt", "r")
            self.cn = datacn.read()
            datacn.close()
        else:
            print("We are missing the cities file.")
            exit()

    @commands.command(description="Find TOS-breaking content in the channel.")
    async def search(self, ctx, guild_id: int):
        await ctx.send('starting')
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
                    if lname in msg:
                        await ctx.send(f"Message was deleted!\n{msg}")
                        delcnt += 1
                        await message.delete()
                        delmsg = True
                        break

                for cname in cna:
                    if delmsg:
                        break
                    if cname in msg:
                        await ctx.send(f"Message was deleted!\n{msg}")
                        delcnt += 1
                        await message.delete()
                        delmsg = True
                        break

                for fname in fna:
                    if delmsg:
                        break
                    if fname in msg:
                        await ctx.send(f"Message was deleted!\n{msg}")
                        delcnt += 1
                        await message.delete()
                        delmsg = True
                        break

                if "pastebin.com" in msg or "doxbin.org" in msg:
                    if delmsg:
                        break
                    await ctx.send(f"Message was deleted!\n{msg}")
                    delcnt += 1
                    await message.delete()
                    delmsg = True
                    break


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
