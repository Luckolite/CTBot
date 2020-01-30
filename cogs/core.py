import asyncio

import discord
from discord.ext import commands

from utils import colors


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.suggest_channel_id = 672135121469571092

    @commands.command(name='info', description='Information about the server')
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def info(self, ctx):
        embed = discord.Embed(
            title = 'Information',
            description = 'Information about the server',
            color = discord.Color.blue()
        )

        embed.set_footer(text='Information')
        embed.add_field(name='Whos confirmed to contribute so far:', value='Luck#1574, elongated muskrat#0001, ProgrammerPlays#8264')
        embed.add_field(name='Whos going to contribute:', value='Boris NL#3982, Tother#5201, Rogue#2754, Lefton#7913, Lach993#4250')
        await ctx.send(embed=embed)
        
    @commands.command(name='suggest', description='submit a suggestion')
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion):
        """ submit a suggestion to a dedicated channel """
        channel = self.bot.get_channel(self.suggest_channel_id)
        e = discord.Embed(color=colors.theme())
        e.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        e.description = str(ctx.author.id)
        e.add_field(name='Suggestion', value=suggestion)
        msg = await channel.send(embed=e)
        e.set_footer(text=str(msg.id))
        await msg.edit(embed=e)
        await ctx.send(f"Sent your suggestion to the dev server. "
                       f"Use `ct!edit {msg.id} your_modified_suggestion` to update it")

    @commands.command(name='edit', description='edit a suggestion')
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def edit(self, ctx, msg_id: int, *, new_suggestion):
        """ edit an existing suggestion """
        channel = self.bot.get_channel(self.suggest_channel_id)
        try:
            msg = await channel.fetch_message(msg_id)
        except discord.errors.NotFound:
            return await ctx.send("There's no suggestion under that id")
        e = msg.embeds[0]
        e.fields[0].value = new_suggestion
        await msg.edit(embed=e)
        await ctx.send("Updated your suggestion")

    @commands.command(name='help', hidden=True)
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    async def help(self, ctx, command=None):
        """ help menu sorted by cog/class name """
        async def add_reactions(msg):
            """ add reactions in the background to speed things up """
            for emoji in emojis:
                await msg.add_reaction(emoji)

        index = {}
        for cmd in [cmd for cmd in self.bot.commands if not cmd.hidden]:
            category = type(cmd.cog).__name__
            if category not in index:
                index[category] = {}
            index[category][cmd.name] = cmd.description
        if command and command not in index.keys():
            for cmd in self.bot.commands:
                if cmd.name == command:
                    if not cmd.usage:
                        return await ctx.send("That command has no usage")
                    return await ctx.send(embed=cmd.usage)
            return await ctx.send("There's no help for that command")

        default = discord.Embed(color=colors.theme())
        default.set_author(name='Help Menu', icon_url=self.bot.user.avatar_url)
        default.set_thumbnail(url=ctx.guild.icon_url)
        value = '\n'.join([
            f'• {category} - {len(commands)} commands' for category, commands in index.items()
        ])
        default.add_field(name='◈ Categories', value=value)

        embeds = [default]
        for category, commands in index.items():
            e = discord.Embed(color=colors.theme())
            e.set_author(name=category, icon_url=self.bot.user.avatar_url)
            e.set_thumbnail(url=ctx.guild.icon_url)
            e.description = '\n'.join([
                f"\n• {cmd} - `{desc}`" for cmd, desc in commands.items()
            ])
            embeds.append(e)

        pos = 0
        if command:
            pos = [c.lower() for c in index.keys()].index(command.lower()) + 1
        msg = await ctx.send(embed=embeds[pos])
        emojis = ['⏪', '⏩', '🔁']
        self.bot.loop.create_task(add_reactions(msg))
        while True:
            def pred(reaction, user):
                return user == ctx.author and str(reaction.emoji) in emojis
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=pred)
            except asyncio.TimeoutError:
                return await msg.clear_reactions()
            else:
                emoji = str(reaction.emoji)
                if emoji == emojis[0]:
                    pos -= 1
                elif emoji == emojis[1]:
                    pos += 1
                elif emoji == emojis[2]:
                    pos = 0

                if pos > len(embeds) - 1:
                    pos = len(embeds) - 1
                if pos < 0:
                    pos = 0

                embeds[pos].set_footer(text=f'Page {pos + 1}/{len(embeds)}')
                await msg.edit(embed=embeds[pos])
                await msg.remove_reaction(reaction, ctx.author)


def setup(bot):
    bot.add_cog(Core(bot))
