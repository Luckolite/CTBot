owner_ids = {
    'Elon': 544911653058248734,
    'Luck': 264838866480005122
}
dev_ids = {
    'Elon': 544911653058248734,
    'Luck': 264838866480005122,
    'Tother': 355026215137968129,
    'Rogue': 295388694167289856,
    'Daichi': 239381528893718539
}

def owner(ctx):
    return ctx.author.id in dev_ids.values()
