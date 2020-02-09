from discord import Color


def bytes2human(n):
    """Converts the number of bytes into a more convenient format."""
    symbols = ("KB", "MB", "GB", "TB", "PT", "EB", "ZB", "YB")
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return "%.1f%s" % (value, s)
    return "%sB" % n


def theme_color(ctx):
    """Returns the theme color."""
    return Color(int(ctx.bot.config["theme"][1:], 16))
