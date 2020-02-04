import asyncio
import json
import traceback
from os import path

import discord
from discord.ext import commands
from discord.ext.commands import ExtensionError

from utils import checks


class CTBot(commands.Bot):
    def __init__(self, **options):
        if path.isfile('./data/coindb.json'):
            with open('./data/coindb.json') as f:
                self.coindb = json.load(f)
        else:
            with open('./data/coindb.json', 'w') as f:
                json.dump({}, f, ensure_ascii=False)

        if not path.isfile('./data/config.json'):
            print('./data/config missing! Please, create it.')
            exit()
        with open('./data/config.json') as f:
            self.config = json.load(f)

        super().__init__(self.config['prefix'], **options)

        # bot.remove_command('help')

    def save_coindb(self):
        with open('./data/coindb.json', 'w') as f:
            json.dump(self.coindb, f, ensure_ascii=False)

    def run(self):
        super().run(self.config['token'])


bot = CTBot(case_insensitive=True)
bot.remove_command('help')
initial_extensions = [
    'core', 'error_handler', 'lockdown', 'appeals', 'dev', 'coin', 'moderator'
]
errors = []


async def status_task():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name='Back Online'))
    while True:
        activities = bot.config['activities']
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

    checks.setup(bot)

    print('Logging in')
    bot.run()
