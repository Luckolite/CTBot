from datetime import datetime, timedelta
from random import randrange

import discord
from discord.ext import commands

from bot import CTBot
from utils.utils import LogLevel


class Levels(commands.Cog):
    def __init__(self, bot: CTBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.author.bot:
            if str(message.guild.id) not in self.bot.levels:
                self.bot.levels[str(message.guild.id)] = {}
            if str(message.author.id) not in self.bot.levels[str(message.guild.id)]:
                self.bot.levels[str(message.guild.id)][str(message.author.id)] = {
                    "timestamp": 0,
                    "xp": 0,
                    "level": 0,
                }
            xp = self.bot.levels[str(message.guild.id)][str(message.author.id)]
            if message.created_at - datetime.fromtimestamp(xp["timestamp"]) > timedelta(
                    minutes=2
            ):
                rand = randrange(10)
                if rand == 0:
                    xp["timestamp"] = message.created_at.timestamp()
                    add = randrange(10, 16)
                    xp["xp"] += add
                    if xp["xp"] >= int(200 * 1.32 ** (xp["level"]) - 100):
                        xp["level"] += 1
                        await self.bot.log(
                            "Levels",
                            f"{message.author.mention} leveled up to {xp['level']}",
                            LogLevel.DEBUG,
                        )
                        await message.channel.send(
                            f"{message.author.id}, you leveled up to {xp['level']}!"
                        )
                    else:
                        await self.bot.log(
                            "Levels",
                            f"Gave {message.author.mention} {add} xp",
                            LogLevel.DEBUG,
                        )
            await self.bot.save()


def setup(bot):
    bot.add_cog(Levels(bot))
