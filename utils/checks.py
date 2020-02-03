owner_ids = {
    'Elon': 544911653058248734,
    'Luck': 264838866480005122
}
dev_ids = {
    'Elon': 544911653058248734,
    'Luck': 264838866480005122,
    'Tother': 355026215137968129,
    'Rogue': 295388694167289856,
    'Daichi': 239381528893718539,
    'Programmer': 607776237737345044,
    'korochun': 308628182213459989
}


def owner(ctx):
    return ctx.author.id in owner_ids.values()


def dev(ctx):
    return ctx.author.id in dev_ids.values()
