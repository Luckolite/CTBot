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


def get_color(bot, status="info"):
    """Returns the theme color."""
    color = bot.config["colors"][status.lower()]
    if color[0] == "#":
        if len(color) == 4:
            return Color(int("".join([x * 2 for x in color[1:]]), 16))
        else:
            return Color(int(color[1:], 16))
    return Color(color)
