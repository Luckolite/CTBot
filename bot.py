import asyncio
import json
import traceback
from os import path

import discord
from discord.ext import commands

#if not path.isfile('./data/coindb.json'):
#    print('You need to make the coin database')
#    exit()
#with open('./data/coindb.json') as c:
#    coindb = json.load(c) # type: array
if not path.isfile('./data/config.json'):
    print('You need to set the config in /data/ first')
    exit()
with open('./data/config.json', 'r') as f:
    config = json.load(f)  # type: dict

bot = commands.Bot(command_prefix=config['prefix'], case_insensitive=True)
bot.remove_command('help')
initial_extensions = [
    'core', 'error_handler', 'lockdown', 'appeals', 'dev', 'coin'
]
errors = []


async def status_task():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name='Back Online'))
    while True:
        activities = ['With Crafting Tables']
        for activity in activities:
            await asyncio.sleep(15)
            await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=activity))


@bot.event
async def on_ready():
    bot.loop.create_task(status_task())
    print('Logged in as', bot.user, "with user id", bot.user.id)
    for error in errors:
        print(error) 

if __name__ == '__main__':
    for cog in initial_extensions:
        try:
            bot.load_extension(f'cogs.{cog}')
            print(f'Loaded {cog}')
        except:
            errors.append([cog, str(traceback.format_exc())])
            print(f'Failed to load {cog}')
print('Logging in')
bot.run(config['token'])
