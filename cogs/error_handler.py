import json
import sys
import traceback
from time import time

import discord
from discord.ext import commands

from utils import colors


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cd = {}

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        full_traceback = str(sys.exc_info())
        e = discord.Embed(color=discord.Color.red())
        e.title = f"Error in {event}"
        e.description = args
        e.add_field(
            name='Keyword Exception Arguments',
            value=str(json.loads(kwargs, indent=2)),
            inline=False
        )
        for text_group in [full_traceback[i:i + 1000] for i in range(0, len(full_traceback), 1000)]:
            e.add_field(name='Traceback', value=text_group, inline=False)
        print(full_traceback)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        ignored = (commands.CommandNotFound, commands.NoPrivateMessage, discord.errors.NotFound)
        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'`{ctx.command}` has been disabled.')
        elif isinstance(error, commands.BadArgument):
            return await ctx.send(error)
        elif isinstance(error, commands.CommandOnCooldown):
            user_id = str(ctx.author.id)
            await ctx.message.add_reaction('⏳')
            if user_id not in self.cd:
                self.cd[user_id] = 0
            if self.cd[user_id] < time() - 10:
                await ctx.send(error)
            self.cd[user_id] = time() + 10
        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(error)
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('You can\'t run this command!')
            return await ctx.message.add_reaction('⚠')
        elif isinstance(error, discord.errors.Forbidden):
            bot = ctx.guild.me
            if ctx.channel.permissions_for(bot).send_messages:
                return await ctx.send(error)
            elif ctx.channel.permissions_for(bot).add_reactions:
                return await ctx.message.add_reaction("⚠")
        elif isinstance(error, KeyError):
            return await ctx.send(f'No data under the key `{error}`')
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            e = discord.Embed(color=colors.theme())
            e.title = 'Uh oh...There was an error!'
            e.description = f'{error}'
            await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
