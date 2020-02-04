from discord import Color


def bytes2human(n):
    symbols = ('kb', 'mb', 'gb', 'tb', 'pb', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def theme_color(ctx):
    return Color(int(ctx.bot.config['theme'][1:], 16))
