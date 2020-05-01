import asyncio
import json
import sys
import traceback
from datetime import datetime
from gzip import compress
from random import choice

import discord
from discord.ext import commands
from discord_sentry_reporting import use_sentry

from bot import CTBot
from utils import utils
from utils.utils import LogLevel

log_name = datetime.now().strftime("logs/%d-%m-%Y %H:%M:%S.log.gz")
logfile = open("latest.log", "a+")


def log(title: str, description: str, level: utils.LogLevel = utils.LogLevel.INFO):
    print(
        f"[{datetime.now().strftime('%H:%M:%S')}] [{title}/{level.name}]: {description}",
        file=sys.stdout if level < utils.LogLevel.ERROR else sys.stderr,
    )
    print(
        f"[{datetime.now().strftime('%H:%M:%S')}] [{title}/{level.name}]: {description}",
        file=logfile,
    )
    logfile.flush()


bot = CTBot(log_func=log, case_insensitive=True)
errors = []


async def status_task():
    """Randomly changes status every 15 seconds."""
    while True:
        await asyncio.sleep(15)
        activity = choice(bot.config["activities"])
        await bot.change_presence(
            activity=discord.Activity(
                name=activity["name"],
                type=discord.ActivityType.__getitem__(activity["status"]),
            )
        )


@bot.event
async def on_ready():
    for ext, error in errors:
        await bot.log(
            f"Load", f"Error loading `{ext}`: ```py\n{error}```", utils.LogLevel.ERROR
        )

    await bot.log(f"Login", f"Logged in as {bot.user} with user id {bot.user.id}")
    bot.loop.create_task(status_task())


def main():
    with open("config/config.json") as f:
        dat = json.load(f)
    if not dat["sentry_dsn"] or dat["sentry_dsn"] != "nO":
        use_sentry(
            bot,  # it is typically named client or bot
            dsn=str(dat["sentry_dsn"])
            # put in any sentry keyword arguments (**kwargs) here
        )

    initial_extensions = [
        "cogs.appeals",
        "cogs.autoreply",
        "cogs.censor",
        "cogs.chat",
        "cogs.coin",
        "cogs.core",
        "cogs.dev",
        "cogs.error_handler",
        "cogs.levels",
        "cogs.lockdown",
        "cogs.memes",
        "cogs.moderation",
        "cogs.applications",
        # "cogs.search",
        "cogs.verify",
        "utils.checks",
        "utils.corona",
    ]
    for ext in initial_extensions:
        try:
            bot.load_extension(ext)
            log("Load", f"Loaded {ext}")
        except commands.ExtensionError:
            errors.append((ext, str(traceback.format_exc())))
            log("Load", f"Failed to load {ext}", LogLevel.ERROR)

    log("Login", "Logging in")
    while True:
        try:
            bot.run()
        except discord.errors.LoginFailure:
            log("Login", f"Login failed:\n{traceback.format_exc()}", LogLevel.ERROR)
            return
        except SystemExit:
            log("Stop", "Stopped bot")
            bot.save()
            logfile.close()
            with open("latest.log") as latest, open(log_name, "wb+") as compressed:
                compressed.write(compress(latest.read()))


if __name__ == "__main__":
    main()

#__#

