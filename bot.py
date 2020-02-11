import asyncio
from datetime import datetime
import json
import traceback
from os import path
from random import choice

import discord
from discord.ext import commands
from discord.ext.commands import ExtensionError

from utils import utils


class CTBot(commands.Bot):
    def __init__(self, **options):
        self.config = None
        self.coindb = None
        self.ldb = None
        self.xpdb = None

        self.load_config()

        super().__init__(
            self.config["prefix"], activity=discord.Game(name="Back Online"), **options
        )

        self.remove_command("help")

    def load_config(self):
        if path.isfile("data/coindb.json"):
            with open("data/coindb.json") as f:
                self.coindb = json.load(f)
        else:
            with open("data/coindb.json", "w") as f:
                json.dump({}, f, ensure_ascii=False)

        with open("config/config.json") as f:
            self.config = json.load(f)

        if path.isfile("data/ldb.json"):
            with open("data/ldb.json") as f:
                self.ldb = json.load(f)
        else:
            with open("data/ldb.json", "w") as f:
                json.dump({}, f, ensure_ascii=False)

        if path.isfile("data/xpdb.json"):
            with open("data/xpdb.json") as f:
                self.xpdb = json.load(f)
        else:
            with open("data/xpdb.json", "w") as f:
                json.dump({}, f, ensure_ascii=False)

    def save_coindb(self):
        """Saves the coin database."""
        with open("data/coindb.json", "w") as f:
            json.dump(self.coindb, f, ensure_ascii=False)

    def save_ldb(self):
        with open("data/ldb.json", "w") as f:
            json.dump(self.coindb, f, ensure_ascii=False)

    def save_xpdb(self):
        with open("data/ldb.json", "w") as f:
            json.dump(self.coindb, f, ensure_ascii=False)

    def run(self):
        super().run(self.config["token"])

    async def reload(self):
        """Reloads all extensions."""
        await self.change_presence(
            status=discord.Status.dnd, activity=discord.Game(name="Reloading")
        )
        self.load_config()
        self.command_prefix = self.config["prefix"]
        await self.log("Reload", "Reloaded config")
        errors = []
        for ext in self.extensions:
            try:
                self.reload_extension(ext)
                print(f"Reloaded {ext}...")
            except ExtensionError:
                errors.append((ext, str(traceback.format_exc())))
                print(f"Failed to reload {ext}")
        for cog, error in errors:
            await bot.log(f"Error reloading {cog}", f"```{error}```", "error")

        await self.change_presence(
            status=discord.Status.online, activity=discord.Game(name="Back Online")
        )

    async def log(self, title, description, status="info"):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [{title}/{status.upper()}]: {description}")
        e = discord.Embed(
            color=utils.get_color(self, status),
            title=title,
            description=description[:1000]
        )
        for text_group in [
            description[i: i + 1000] for i in range(1000, len(description), 1000)
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
    bot.server = bot.get_guild(bot.config["ids"]["server"])
    bot.loop.create_task(status_task())
    await bot.log(f"Login", f"Logged in as {bot.user} with user id {bot.user.id}")
    for cog, error in errors:
        await bot.log(f"Error loading {cog}", f"```{error}```", "error")


def main():
    initial_extensions = [
        "cogs.appeals",
        "cogs.autoresponse",
        "cogs.coin",
        "cogs.core",
        "cogs.dev",
        "cogs.error_handler",
        "cogs.lockdown",
        "cogs.moderation",
        "utils.checks",
        "cogs.levels",
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


if __name__ == "__main__":
    main()
