import asyncio
import json
import traceback
from datetime import datetime
from os import path
from random import choice

import discord
from discord.ext import commands
from discord.ext.commands import ExtensionError

from utils import utils


class CTBot(commands.Bot):
    def __init__(self, **options):
        self.config = {}
        self.data = "appeal_ban", "coin", "core_commands", "levels", "levels_xp"
        for name in self.data:
            self.__dict__[name] = {}

        self.load()

        super().__init__(
            commands.when_mentioned_or(self.config["prefix"]),
            activity=discord.Game(name="Back Online"),
            **options,
        )

        self.remove_command("help")

    def load(self):
        with open("config/config.json") as f:
            old_config = self.config
            self.config = json.load(f)
            for k in old_config:  # To only add fields, not replace the existing ones
                self.config[k] = old_config[k]

        self.save()
        for name in self.data:
            if path.isfile(name):
                with open(f"data/{name}.json") as f:
                    self.__dict__[name] = json.load(f)
            else:
                with open(f"data/{name}.json", "w") as f:
                    json.dump(self.__dict__[name], f, ensure_ascii=False)

    def save(self):
        for name in self.data:
            with open(f"data/{name}.json", "w") as f:
                json.dump(self.__dict__[name], f, ensure_ascii=False)

    def run(self):
        super().run(self.config["token"])

    async def reload(self):
        """Reloads all extensions."""
        await self.change_presence(
            status=discord.Status.dnd, activity=discord.Game(name="Reloading")
        )
        self.load()
        self.command_prefix = self.config["prefix"]
        await self.log("Reload", "Reloaded config")
        errors = []
        for ext in self.extensions:
            try:
                self.reload_extension(ext)
                await self.log("Reload", f"Reloaded `{ext}`...")
            except ExtensionError:
                errors.append((ext, str(traceback.format_exc())))
                await self.log("Reload", f"Failed to reload `{ext}`")
        for ext, error in errors:
            await bot.log(
                f"Reload", f"Error reloading `{ext}`:\n```{error}```", "error"
            )

        await self.change_presence(
            status=discord.Status.online, activity=discord.Game(name="Back Online")
        )

    async def log(self, title, description, status="info"):
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] [{title}/{status.upper()}]: {description}"
        )
        e = discord.Embed(
            color=utils.get_color(self, status),
            title=title,
            description=description[:1000],
        )
        for text_group in [
            description[i : i + 1000] for i in range(1000, len(description), 1000)
        ]:
            e.add_field(name=".", value=text_group)
        await self.get_channel(self.config["ids"]["log_channel"]).send(embed=e)


bot = CTBot(case_insensitive=True)
errors = []


async def status_task():
    """Randomly changes status every 15 seconds."""
    while True:
        await asyncio.sleep(15)
        activity = choice(bot.config["activities"])
        await bot.change_presence(
            activity=discord.Activity(
                name=activity["name"], type=discord.ActivityType[activity["status"]]
            )
        )


@bot.event
async def on_ready():
    for ext, error in errors:
        await bot.log(f"Load", f"Error loading `{ext}`:\n```{error}```", "error")

    await bot.log(f"Login", f"Logged in as {bot.user} with user id {bot.user.id}")
    bot.loop.create_task(status_task())


def main():
    initial_extensions = [
        "cogs.appeals",
        "cogs.autoresponse",
        "cogs.coin",
        "cogs.core",
        "cogs.dev",
        "cogs.error_handler",
        "cogs.levels",
        "cogs.lockdown",
        "cogs.moderation",
        "utils.checks",
    ]
    for ext in initial_extensions:
        try:
            bot.load_extension(ext)
            print(f"Loaded {ext}")
        except ExtensionError:
            errors.append((ext, str(traceback.format_exc())))
            print(f"Failed to load {ext}")

    print("Logging in")
    bot.run()
    bot.save()


if __name__ == "__main__":
    main()
