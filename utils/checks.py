import json
from discord.ext import commands


class Checks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def owner(self, ctx):
        """A bot owner command check."""
        return ctx.author.id in self.bot.config["owners"].values()

    def dev(self, ctx):
        """A bot developer command check."""
        return ctx.author.id in self.bot.config["devs"].values()

    def command_is_enabled(self):
        async def predicate(ctx):
            with open("./data/disabled_commands.json") as f:
                config = json.load(f)  # type: dict
            guild_id = str(ctx.guild.id)
            if guild_id not in config:
                return True
            conf = config[guild_id]
            cmd = ctx.command.name
            if cmd in conf["global"]:
                return False
            channel_id = str(ctx.channel.id)
            if channel_id in conf["channels"]:
                if cmd in conf["channels"][channel_id]:
                    return False
            if ctx.channel.category:
                channel_id = str(ctx.channel.category.id)
                if channel_id in conf["categories"]:
                    if cmd in conf["categories"][channel_id]:
                        return False
            return True

        return commands.check(predicate)


checks = None


def setup(bot):
    global checks
    checks = Checks(bot)
    bot.add_cog(checks)
