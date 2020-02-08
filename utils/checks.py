ids = {
    'owner': {},
    'dev': {}
}


def owner(ctx):
    """A bot owner command check."""
    return ctx.author.id in ids['owner'].values()


def dev(ctx):
    """A bot developer command check."""
    return ctx.author.id in ids['dev'].values()


def setup(bot):
    ids['owner'] = bot.config['owners']
    ids['dev'] = bot.config['devs']
