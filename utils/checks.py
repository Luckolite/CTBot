ids = {
    'owner': {},
    'dev': {}
}


def owner(ctx):
    return ctx.author.id in ids['owner'].values()


def dev(ctx):
    return ctx.author.id in ids['dev'].values()


def setup(bot):
    ids['owner'] = bot.config['owners']
    ids['dev'] = bot.config['devs']
