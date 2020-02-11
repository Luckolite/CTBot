import asyncio
import json
import os
from os import path
from typing import *

import discord
import psutil
from discord.ext import commands

from utils import checks, utils


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.suggest_channel_id = bot.config["suggestion_channel"]

    @commands.command(description="Displays information about the bot.")
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def info(self, ctx):
        """Displays information about the bot."""
        e = discord.Embed(color=utils.theme_color(ctx))
        c = utils.bytes2human
        p = psutil.Process(os.getpid())
        perms = discord.Permissions()
        perms.update(
            embed_links=True, kick_members=True, ban_members=True, manage_roles=True
        )
        inv = (
            f"https://discordapp.com/oauth2/authorize"
            f"?client_id={self.bot.user.id}"
            f"&permissions={perms.value}"
            f"&scope=bot"
        )

        e.set_author(name="CTBot Information", icon_url=self.bot.user.avatar_url)
        e.set_thumbnail(url=self.bot.server.icon_url)
        e.description = (
            f"A handy bot that's dedicated its code to the crafting table religion"
        )
        e.add_field(
            name="◈ Github",
            value="> If you wish to report bugs, suggest changes or contribute to the development "
                  "[visit the repo](https://github.com/FrequencyX4/CTBot)",
            inline=False,
        )
        e.add_field(
            name="◈ Credits",
            value="\n".join(
                [
                    f"• [{self.bot.get_user(user_id)}](https://discordapp.com/channels/@me/{user_id})"
                    for user_id in self.bot.config["devs"].values()
                ]
            ),
        )
        e.add_field(
            name="◈ Links",
            value=f"• [Crafting Table]({self.bot.config['server_inv']})\n"
                  f"• [Github](https://github.com/FrequencyX4/CTBot)\n"
                  f"• [Dev Discord]({self.bot.config['dev_server_inv']})\n"
                  f"• [Invite Me]({inv})",
        )
        e.set_footer(
            text=f"CPU: {psutil.cpu_percent()}% | Ram: {c(p.memory_full_info().rss)} ({round(p.memory_percent())}%)",
            icon_url="https://media.discordapp.net/attachments/514213558549217330/514345278669848597/8yx98C.gif",
        )
        await ctx.send(embed=e)

    @commands.command(description="Submits a suggestion.")
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion):
        """Submits a suggestion to the dedicated channel."""
        channel = self.bot.get_channel(self.suggest_channel_id)
        embed = discord.Embed(color=utils.theme_color(ctx.bot))
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        embed.add_field(name="Suggestion", value=suggestion)
        msg = await channel.send(embed=embed)
        embed.set_footer(text=f"id: {msg.id}")
        await msg.edit(embed=embed)
        await ctx.send(
            f"Sent your suggestion to the dev server. "
            f"Use `ct!edit {msg.id} Edited suggestion` to update it"
        )

    @commands.command(description="Edits a suggestion.")
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def edit(self, ctx, msg_id: int, *, new_suggestion):
        """Edits an existing suggestion."""
        channel = self.bot.get_channel(self.suggest_channel_id)
        try:
            msg = await channel.fetch_message(msg_id)
        except discord.errors.NotFound:
            return await ctx.send("There's no suggestion under that id")
        e = msg.embeds[0]
        if str(ctx.author) == e.author or checks.dev(ctx):
            e.set_field_at(0, name="Suggestion", value=f"{new_suggestion} *(edited)*")
            await msg.edit(embed=e)
            await ctx.send("Updated your suggestion")
        else:
            await ctx.send("You can't edit this suggestion")

    @commands.command(hidden=True)
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    async def help(self, ctx, command=None):
        """Displays the help menu sorted by cog/class name."""

        async def add_reactions(message):
            """Add reactions in the background to speed things up."""
            for emoji_ in emojis:
                await message.add_reaction(emoji_)

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

        default = discord.Embed(color=utils.theme_color(ctx))
        default.set_author(name="Help Menu", icon_url=self.bot.user.avatar_url)
        default.set_thumbnail(url=ctx.guild.icon_url)
        value = "\n".join(
            [
                f"• {category} - {len(commands_)} commands"
                for category, commands_ in index.items()
            ]
        )
        default.add_field(name="◈ Categories", value=value)

        embeds = [default]
        for category, commands_ in index.items():
            e = discord.Embed(color=utils.theme_color(ctx))
            e.set_author(name=category, icon_url=self.bot.user.avatar_url)
            e.set_thumbnail(url=ctx.guild.icon_url)
            e.description = "\n".join(
                [f"\n• {cmd} - `{desc}`" for cmd, desc in commands_.items()]
            )
            embeds.append(e)

        pos = 0
        if command:
            pos = [c.lower() for c in index.keys()].index(command.lower()) + 1
        await ctx.message.delete()
        msg = await ctx.send(embed=embeds[pos])
        emojis = ["⏮", "◀️", "⏹", "▶️", "⏭"]
        self.bot.loop.create_task(add_reactions(msg))
        while True:

            def pred(react, usr):
                return (
                        react.message.id == msg.id
                        and usr == ctx.author
                        and str(react.emoji) in emojis
                )

            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=60.0, check=pred
                )
            except asyncio.TimeoutError:
                return await msg.clear_reactions()

            emoji = str(reaction.emoji)
            await msg.remove_reaction(reaction, ctx.author)
            i = emojis.index(emoji)
            if pos > 0 and i < 2:
                if i == 0:
                    pos = 0
                else:
                    pos -= 1
            elif pos < len(embeds) - 1 and i > 2:
                if i == 3:
                    pos += 1
                else:
                    pos = len(embeds) - 1
            elif i == 2:
                return await msg.delete()
            else:
                continue

            embeds[pos].set_footer(text=f"Page {pos + 1}/{len(embeds)}")
            await msg.edit(embed=embeds[pos])

    @commands.command(name="enable", enabled=False)
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def enable(
            self,
            ctx,
            command,
            location: Union[discord.TextChannel, discord.CategoryChannel] = None,
    ):
        """Enable or commands in a channel, or category"""
        fp = "./data/disabled_commands.json"
        if not path.isfile(fp):
            with open(fp, "w") as f:
                json.dump({}, f, ensure_ascii=False)
        with open(fp) as f:
            config = json.load(f)  # type: dict
        guild_id = str(ctx.guild.id)
        if guild_id not in config:
            config[guild_id] = {"global": [], "channels": {}, "categories": {}}
        conf = config[guild_id]
        channel_id = str(ctx.channel.id)
        if not location:
            if command in conf["global"]:
                conf["global"].remove(command)
                await ctx.send(f"Globally enabled {command}")
            elif channel_id in conf["channels"]:
                if command in conf["channels"][channel_id]:
                    conf["channels"][channel_id].remove(command)
                    await ctx.send(f"Enabled {command} in {ctx.channel.mention}")
            elif ctx.channel.category:
                category_id = str(ctx.channel.category.id)
                if category_id in conf["categories"]:
                    if command in conf["categories"][category_id]:
                        conf["categories"][category_id].remove(category_id)
                        await ctx.send(f"Enabled {command} in {ctx.channel.category}")
        elif isinstance(location, discord.TextChannel):
            channel_id = str(location.id)
            if channel_id not in conf["channels"]:
                return await ctx.send("That channel has no disabled commands")
            if command not in conf["channels"][channel_id]:
                return await ctx.send(f"{command} isn't disabled in that channel")
            conf["channels"][channel_id].remove(command)
        elif isinstance(location, discord.CategoryChannel):
            channel_id = str(location.id)
            if channel_id not in conf["categories"]:
                return await ctx.send("That category has no disabled commands")
            if command not in conf["categories"][channel_id]:
                return await ctx.send(f"{command} isn't disabled in that category")
            conf["categories"][channel_id].remove(command)
        with open(fp, "w") as f:
            json.dump(config, f, ensure_ascii=False)

    @commands.command(name="disable", enabled=False)
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def disable(
            self,
            ctx,
            command,
            location: Union[discord.TextChannel, discord.CategoryChannel] = None,
    ):
        """Enable or commands in a channel, or category"""
        fp = "./data/disabled_commands.json"
        if not path.isfile(fp):
            with open(fp, "w") as f:
                json.dump({}, f, ensure_ascii=False)
        with open(fp) as f:
            config = json.load(f)  # type: dict
        guild_id = str(ctx.guild.id)
        if guild_id not in config:
            config[guild_id] = {"global": [], "channels": {}, "categories": {}}
        conf = config[guild_id]
        channel_id = str(ctx.channel.id)
        if not location:
            if channel_id not in conf["channels"]:
                conf["channels"][channel_id] = []
            if command not in conf["global"]:
                conf["global"].append(command)
                await ctx.send(f"Globally disabled {command}")
            elif command not in conf["channels"][channel_id]:
                conf["channels"][channel_id].append(command)
                await ctx.send(f"Disabled {command} in {ctx.channel.mention}")
            elif ctx.channel.category:
                category_id = str(ctx.channel.category.id)
                if category_id not in conf["categories"]:
                    conf["categories"][category_id] = []
                if command not in conf["categories"][category_id]:
                    conf["categories"][category_id].append(category_id)
                    await ctx.send(f"Disabled {command} in {ctx.channel.category}")
        elif isinstance(location, discord.TextChannel):
            channel_id = str(location.id)
            if channel_id not in conf["channels"]:
                conf["channels"][channel_id] = []
            if command in conf["channels"][channel_id]:
                return await ctx.send(f"{command} is already disabled in that channel")
            conf["channels"][channel_id].append(command)
        elif isinstance(location, discord.CategoryChannel):
            channel_id = str(location.id)
            if channel_id not in conf["categories"]:
                conf["categories"][channel_id] = []
            if command in conf["categories"][channel_id]:
                return await ctx.send(f"{command} is already disabled in that category")
            conf["categories"][channel_id].append(command)
        config[guild_id] = conf
        with open(fp, "w") as f:
            json.dump(config, f, ensure_ascii=False)


def setup(bot):
    bot.add_cog(Core(bot))
