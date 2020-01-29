from time import time
import traceback
import sys
import discord
from discord.ext import commands
from utils import colors


class error_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cd = {}

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
            await ctx.send(error)
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
    bot.add_cog(error_handler(bot))
