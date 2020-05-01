import json
import datetime
import sys
import traceback
from time import time
from requests import get

import discord
from discord.ext import commands, tasks


def get_corona_stats():
    r = get("http://corona.lmao.ninja/countries")
    if r.status_code == 200:
        data = {}
        for elem in r.json():
            data[elem["country"]] = elem
        return data
    else:
        return None


def get_corona_total():
    r = get("http://corona.lmao.ninja/all")
    if r.status_code == 200:
        return r.json()
    else:
        return None


class CoronaStats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.stats = get_corona_stats()
        self.bot.stats["all"] = get_corona_total()
        self.refresh.start()

    @commands.command(
        description="shows cases per state",
        help="Shows "
        "all the stats available for the provided state"
        "the OTP again (and you should change it asap). Will always DM",
    )
    async def corona(self, ctx: commands.Context, country: str):
        if country not in self.bot.stats:
            raise KeyError
        data = self.bot.stats[country]
        embed = discord.Embed()
        embed.set_footer(text="stay at home retard")
        embed.timestamp = datetime.datetime.utcnow()
        if country == "all":
            embed.set_author(
                name="Total COVID-19 cases",
                icon_url="https://upload.wikimedia.org/wikipedia/commons/7/78/Coronaviruses_004_lores.jpg",
            )
        else:
            embed.set_author(name=country, icon_url=data["countryInfo"]["flag"])
        embed.add_field(name="Total Cases", value=data["cases"])
        embed.add_field(name="Total Deaths", value=data["deaths"])
        embed.add_field(name="Recovered", value=data["recovered"])
        await ctx.send(embed=embed)

    @tasks.loop(minutes=2.0)
    async def refresh(self):
        newdata = get_corona_stats()
        newdata["all"] = get_corona_total()
        if newdata is not None and newdata["all"] is not None:
            self.bot.stats = newdata


def setup(bot):
    bot.add_cog(CoronaStats(bot))
