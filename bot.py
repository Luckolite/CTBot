import asyncio
import json
import traceback
from os import path

import discord
from discord.ext import commands
from discord.ext.commands import ExtensionError

if not path.isfile('./data/coindb.json'):
    with open('./data/coindb.json', 'w') as f:
        json.dump({}, f, ensure_ascii=False)
if not path.isfile('./data/config.json'):
    print('You need to set the config in /data/ first')
    exit()
with open('./data/config.json') as f:
    config = json.load(f)  # type: dict

bot = commands.Bot(command_prefix=config['prefix'], case_insensitive=True)
bot.remove_command('help')
initial_extensions = [
    'core', 'error_handler', 'lockdown', 'appeals', 'dev', 'coin', 'moderator'
]
errors = []


async def status_task():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name='Back Online'))
    while True:
        activities = ['The Valley of Crafting Tables', 'with 4 planks of wood', '2B2T']
        for activity in activities:
            await asyncio.sleep(15)
            if activities.index(activity) == 1:
                status = discord.ActivityType.watching
            else:
                status = discord.Status.online
            await bot.change_presence(status=status, activity=discord.Game(name=activity))


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
        except ExtensionError:
            errors.append([cog, str(traceback.format_exc())])
            print(f'Failed to load {cog}')
print('Logging in')
bot.run(config['token'])
