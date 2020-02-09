import json

import discord

from utils import utils

with open("config/logging.json") as f:
    log_config = json.load(f)


async def banned_words(bot, msg: discord.Message):
    if (
        log_config["enabled"]
        and log_config["banned_word_log"]
        and log_config["log_channel"]
    ):
        await bot.get_channel(log_config["multi_log"][0][1]).send(
            embed=discord.Embed(
                colour=discord.Color(utils.theme_color(bot)),
                title="<a:siren:672086274194276372> Banned Word <a:siren:672086274194276372> - the sirens need to be in "
                "https://discord.gg/Qa2jnXP, just ping me there asking me to invite the bot.",
                description=f"> **Author**: {msg.author.mention} | id: {msg.author.id}\n"
                f"> **Channel**: {msg.channel.mention} | id: {msg.channel.id}\n"
                f"> **MSG ID**: {msg.id}\n"
                f"\n"
                f"> 🎴 Content 🎴\n"
                f"> {msg.content}\n",
            )
        )
