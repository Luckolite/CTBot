import json
import re


import discord
import discord.errors
from discord.ext import commands
from profanity_check import predict

from bot import CTBot
from utils.utils import LogLevel


async def remove_message(message: discord.Message, reason: str, notify: bool = True):
    await message.delete()

    if notify:
        await message.channel.send(
            f"Your message was deleted, because it contains {reason}"
        )


class Censor(commands.Cog):
    def __init__(self, bot: CTBot):
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
        if author.bot:
            return False

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

    @staticmethod
    async def warn(member: discord.member, action: str, content: str):
        await member.send(
            f"Your recent {action} was removed because {content}."
        )

    @commands.Cog.listener("on_message")
    @commands.Cog.listener("on_message_edit")
    async def profanity_filter_ml(self, *args):
        message = args[-1]
        if (
                self.should_run(message.author)
                and self.config["profanity_filter_ml"]
                and predict([message.content]) == [1]
        ):
            await remove_message(message, "a banned word", notify=self.config['notify_on_censor'])
            if self.config["warn_on_censor"]:
                await self.warn(message.author, "message", "it contained a banned word")

    @commands.Cog.listener("on_message")
    @commands.Cog.listener("on_message_edit")
    async def profanity_filter(self, *args):
        message = args[-1]

        if self.should_run(message.author) and self.config["profanity_filter"]:
            match = self.blocked_words_regex.search(message.content)
            if match is not None:
                await remove_message(message, "a banned word", notify=self.config['notify_on_censor'])

                if self.config["warn_on_censor"]:
                    await self.warn(message.author, "message", "it contained a banned word")

                if self.config["debug"]:
                    await self.bot.log(
                        "CENSOR",
                        f"Removed message \"{message.content}\" for \"{match.group(0)}\"",
                        LogLevel.DEBUG
                    )

    @commands.Cog.listener("on_message")
    @commands.Cog.listener("on_message_edit")
    async def message_char_limit(self, *args):
        message = args[-1]
        if self.should_run(message.author) and 0 < self.config[
            "message_char_limit"
        ] <= len(message.content):
            await remove_message(message, "too many symbols", notify=self.config['notify_on_censor'])

            if self.config["warn_on_censor"]:
                await self.warn(message.author, "message", "it exceeded the character limit")

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
                await remove_message(message, "TOO MANY CAPS", notify=self.config['notify_on_censor'])
                if self.config["warn_on_censor"]:
                    await self.warn(
                        message.author, "message", "it exceeded the maximum amount of capitalized letters"
                    )

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
                    await remove_message(message, "a banned URL", notify=self.config['notify_on_censor'])
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
        if self.should_run(after) and self.config["nickname_filter_enabled"] and after.nick is not None:

            if self.config["debug"]:
                await self.bot.log(
                    "CENSOR", f"Running nickname censor on {after}, nickname {after.nick}",
                    LogLevel.DEBUG
                )

            for word in after.nick.lower().split():
                if word.lower() in self.blocked_words:

                    try:
                        await after.edit(
                            nick=None,
                            reason="CENSORED BY CT BOT",
                        )
                    except discord.errors.Forbidden:
                        return

                    if self.config["warn_on_censor"]:
                        await self.warn(after, "nickname", "it contained a banned word")

                    if self.config["debug"]:
                        await self.bot.log(
                            "CENSOR",
                            f"nick: {after.nick} has been blocked because it contains {word}",
                            LogLevel.DEBUG
                        )


def setup(bot: CTBot):
    bot.add_cog(Censor(bot))
