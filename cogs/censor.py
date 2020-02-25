import json
import re

import discord
from discord.ext import commands
from profanity_check import predict


async def remove_message(message: discord.Message, reason: str):
    await message.delete()
    await message.channel.send(
        f"Your message was deleted, because it contains {reason}"
    )


class Censor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("config/censor.json") as f:
            self.config = json.load(f)
        with open("config/blocked_words.txt") as f:
            bw = f.read()
            self.blocked_words = bw.split()

            # Create RegEx from censored words file
            self.blocked_words_regex = re.compile(
                "|".join(map(re.escape, bw.strip().split('\n'))),
                flags=re.IGNORECASE
            )

    def should_run(self, author: discord.Member):
        if (
            self.config["enabled"]
            and author.id not in self.config["word_filter_exception_user_ids"]
            and author.id not in self.config["all_exempt_user_ids"]
        ):
            for role in author.roles:
                if (
                    role.id in self.config["word_filter_exception_role_ids"]
                    or role.id in self.config["all_exempt_roles"]
                ):
                    return False
            return True
        return False

    def warn(self, member):
        raise NotImplementedError("Warns have not been implemented yet")

    @commands.Cog.listener("on_message")
    @commands.Cog.listener("on_message_edit")
    async def profanity_filter_ml(self, *args):
        message = args[-1]
        if (
            self.should_run(message.author)
            and self.config["profanity_filter_ml"]
            and predict([message.content]) == [1]
        ):
            await remove_message(message, "a banned word")
            if self.config["warn_on_censor"]:
                self.warn(message.author)

    @commands.Cog.listener("on_message")
    @commands.Cog.listener("on_message_edit")
    async def profanity_filter(self, *args):
        message = args[-1]
        if self.should_run(message.author) and self.config["profanity_filter"]:
            if self.blocked_words_regex.search(message.content) is not None:
                await remove_message(message, "a banned word")
                if self.config["warn_on_censor"]:
                    self.warn(message.author)

    @commands.Cog.listener("on_message")
    @commands.Cog.listener("on_message_edit")
    async def message_char_limit(self, *args):
        message = args[-1]
        if self.should_run(message.author) and 0 < self.config[
            "message_char_limit"
        ] <= len(message.content):
            await remove_message(message, "too many symbols")
            if self.config["warn_on_censor"]:
                self.warn(message.author)

    @commands.Cog.listener("on_message")
    @commands.Cog.listener("on_message_edit")
    async def caps_limit(self, *args):
        message = args[-1]
        if self.should_run(message.author) and self.config["caps_limit_enabled"]:
            cap_count = 0
            for i in message.content:
                if i.isupper():
                    cap_count += 1
            if cap_count >= self.config["caps_limit"]:
                await remove_message(message, "TOO MANY CAPS")
                if self.config["warn_on_censor"]:
                    self.warn(message.author)

    @commands.Cog.listener("on_message")
    @commands.Cog.listener("on_message_edit")
    async def domain_filter(self, *args):
        message = args[-1]
        if self.should_run(message.author) and self.config["filter_domains"]:
            for word in message.content.split():
                if word.lower() in self.config["domain_blacklist"]:
                    if self.bot.config["debug"]:
                        print(
                            f"Message: {message.content} has been blocked because it contains "
                            f"{word} {message.content.lower().count(word.lower())} time(s)"
                        )
                    await remove_message(message, "a banned URL")
            if len(self.config["domain_whitelist"]) > 0:
                for word in message.content.split():
                    if word.lower() in self.config["domain_whitelist"]:
                        if self.bot.config["debug"]:
                            print(
                                f"Message: {message.content} has been blocked because it contains"
                                f"{word} {message.content.lower().count(word.lower())} time(s)"
                            )

    @commands.Cog.listener("on_member_update")
    async def nick_censor(self, _: discord.Member, after: discord.Member):
        if self.should_run(after) and self.config["nickname_filter_enabled"]:
            for word in after.nick.lower().split():
                if word.lower() in self.blocked_words:
                    await after.edit(
                        nick=self.config["censored_nickname"],
                        reason="CENSORED BY CT BOT",
                    )
                    if self.config["warn_on_censor"]:
                        self.warn(after)
                    if self.config["debug"]:
                        print(
                            f"nick: {after.nick} has been blocked because it contains {word} "
                            f"{after.nick.lower().count(word.lower())} times"
                        )


def setup(bot):
    bot.add_cog(Censor(bot))
