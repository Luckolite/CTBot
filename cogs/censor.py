import json

import discord
from discord.ext import commands
from profanity_check import predict

from utils.logging import banned_words


class Censor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('config/censor.json') as f:
            self.config = json.load(f)
        with open('config/blocked_words.txt') as f:
            self.blocked_words = f.read().split()

    def warn(self, member):
        raise NotImplementedError('Warns have not been implemented yet')

    def should_run(self, author: discord.Member):
        if self.config["enabled"] and author.id not in self.config["word_filter_exception_user_ids"]\
                and author.id not in self.config["all_exempt_user_ids"]:
            for role in author.roles:
                if role.id in self.config["word_filter_exception_role_ids"] or role.id in self.config["all_exempt_roles"]:
                    return False
            return True
        return False

    @commands.Cog.listener('on_message')
    @commands.Cog.listener('on_message_edit')
    async def profanity_filter_ml(self, *args):
        message = args[-1]
        if self.should_run(message.author) and self.config["profanity_filter_ml"] and predict([message.content]) == [1]:
            await message.delete()
            if self.config["warn_on_censor"]:
                self.warn(message.author)

    @commands.Cog.listener('on_message')
    @commands.Cog.listener('on_message_edit')
    async def profanity_filter(self, *args):
        message = args[-1]
        if self.should_run(message.author) and self.config["profanity_filter"]:
            for word in message.content.split():
                if word.lower() in self.blocked_words:
                    await message.delete()
                    if self.config["warn_on_censor"]:
                        self.warn(message.author)

    @commands.Cog.listener('on_message')
    @commands.Cog.listener('on_message_edit')
    async def message_char_limit(self, *args):
        message = args[-1]
        if self.should_run(message.author) and 0 < self.config["message_char_limit"] <= len(message.content):
            await message.delete()
            if self.config["warn_on_censor"]:
                self.warn(message.author)

    @commands.Cog.listener('on_message')
    @commands.Cog.listener('on_message_edit')
    async def caps_limit(self, *args):
        message = args[-1]
        if self.should_run(message.author) and self.config["caps_limit_enabled"]:
            cap_count = 0
            for i in message.content:
                if i.isupper():
                    cap_count += 1
            if cap_count >= self.config["caps_limit"]:
                await message.delete()
                if self.config["warn_on_censor"]:
                    self.warn(message.author)

    @commands.Cog.listener('on_message')
    @commands.Cog.listener('on_message_edit')
    async def word_filter(self, *args):
        message = args[-1]
        if self.should_run(message.author) and self.config["word_filter_enabled"] \
                and message.channel.id not in self.config["word_filter_channel_exceptions_array_ids"]:
            for word in message.content.split():
                if word.lower() in self.blocked_words:
                    if self.bot.config["debug"]:
                        print(
                            f'Message: {message.content} has been blocked because it '
                            f'contains {word} {message.content.lower().count(word.lower())} times')
                        await banned_words(self, message)
                    await message.delete()

    @commands.Cog.listener('on_message')
    @commands.Cog.listener('on_message_edit')
    async def domain_filter(self, *args):
        message = args[-1]
        if self.should_run(message.author) and self.config["filter_domains"]:
            for word in message.content.split():
                if word.lower() in self.config["domain_blacklist"]:
                    if self.bot.config["debug"]:
                        print(
                            f'Message: {message.content} has been blocked because it contains '
                            f'{word} {message.content.lower().count(word.lower())} time(s)')
                    await message.delete()
            if len(self.config["domain_whitelist"]) > 0:
                for word in message.content.split():
                    if word.lower() in self.config["domain_whitelist"]:
                        if self.bot.config["debug"]:
                            print(f'Message: {message.content} has been blocked because it contains'
                                  f'{word} {message.content.lower().count(word.lower())} time(s)')

    @commands.Cog.listener('on_member_update')
    async def nick_censor(self, before: discord.Member, after: discord.Member):
        if self.should_run(after) and self.config["nickname_filter_enabled"]:
            for word in after.nick.lower().split():
                if word.lower() in self.blocked_words:
                    await after.edit(nick=self.config["censored_nickname"], reason="CENSORED BY CT BOT")
                    if self.config["warn_on_censor"]:
                        self.warn(after)
                    if self.config['debug']:
                        print(
                            f'nick: {after.nick} has been blocked because it contains {word} {after.nick.lower().count(word.lower())} times')


def setup(bot):
    bot.add_cog(Censor(bot))
