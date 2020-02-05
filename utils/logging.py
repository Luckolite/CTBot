import json
from os import path

import discord


def get_vars_a():
    if not path.isfile('./data/logging.json'):
        print('You need to set the censor config in ./data/ first')
        exit()
    with open('./data/config.json', 'r') as f:
        botCFG = json.load(f)  # type: dict
    with open('./data/censor.json', 'r') as f:
        censorCFG = json.load(f)  # type: dict
    with open('./data/logging.json', 'r') as f:
        logCFG = json.load(f)  # type: dict
    return logCFG, censorCFG, botCFG


async def banned_words(self, msg: discord.Message):
    embed = discord.Embed(colour=discord.Color(self.bot.config['theme']))
    logCFG, censorCFG, botCFG = get_vars_a()
    if logCFG["enabled"] == "False":
        return
    if logCFG["banned-word-log"] == "False":
        return
    if logCFG["log-channel"] == 0:
        embed.title = "<a:siren:672086274194276372> Banned Word <a:siren:672086274194276372> - the sirens need to be in https://discord.gg/Qa2jnXP, just ping me there asking me to invite the bot.\n"
        embed.description = f'> **Author**: {msg.author.mention} | id: {msg.author.id}\n' \
                            f'> **Channel**: {msg.channel.mention} | id: {msg.channel.id}\n' \
                            f'> **MSG ID**: {msg.id}\n' \
                            f'\n' \
                            f'> 🎴 Content 🎴\n' \
                            f'> {msg.content}\n'
        await self.bot.get_channel(logCFG["multi-log"][0][1]).send(embed=embed)
