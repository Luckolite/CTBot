import asyncio
import json
from os import path
from time import time

import discord
from discord.ext import commands

from utils import utils


class Appeals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # this just defines what `self.bot` is.
        self.path = './config/appeal_blacklist.json'  # the blacklist file
        self.blacklist = {  # this is the blacklist, it allows you to ban users from making appeals!
            # '1234': {
            #     'cooldown': -1,       # a timestamp, when able to submit appeals again
            #     'banned': False       # True if banned from submitting appeals
            # }
        }
        if path.isfile(self.path):  # checks if `self.path` exists
            with open(self.path) as f:
                self.blacklist = json.load(f)  # type: dict
        self.ct_id = bot.config['server']  # server id
        self.channel_id = bot.config['appeal_channel']  # dedicated appeals channel

    def save_data(self):  # for saving the appeals blacklist file data (a function)
        with open(self.path, 'w+') as f:  # opens `self.path` in the mode `w+`
            json.dump(self.blacklist, f)  # dumps in the json to the file.

    @commands.command(name='appeal', description='Requests a ban appeal.')  # defines the command to be `appeal` and sets the description.
    @commands.cooldown(2, 30, commands.BucketType.user)  # the cooldown for the user
    @commands.cooldown(1, 1)  # just look at the docs.
    async def appeal(self, ctx, *, appeal):  # creates the ASYNC function for appeals, this is nessecery for all bot commands.
        """Appeal a ban from the Followers of the Crafting Table."""
        user_id = str(ctx.author.id)  # gets the user id as a string 
        if user_id in self.blacklist:  # if the user id is in the blacklist
            if self.blacklist[user_id]['banned']:  # if the user id is banned
                return await ctx.send("You are banned from submitting appeals!")  # returns with the message
            cooldown = self.blacklist[user_id]['cooldown']  # gets the cooldown of the user if they are not banned from appeals
            if cooldown:  # if there is a cooldown
                cd = cooldown - time()  # get the cooldown at the current time
                if cd > 0:  # if the cooldown is larger than 0
                    msg = "You're on a 2-day cooldown due to your appeal being denied. "  # sets the message
                    if cooldown >= 86000:  # if the cooldown is more than or equal to 86000
                        msg += f"{cooldown // 86000} day, "  # I think this is quite self explanetory
                    if cooldown >= 3600:  # if the cooldown is more than or equal to 3600
                        h = cooldown // 3600  # same as two above
                        msg += f"{h} hour"  # changes things into hours
                        if h % 10 != 1:  # modulo is %, self explanetory from there.
                            msg += 's'  # 's' is appended to the `msg` var
                        msg += ", "  # same thing but with a ', '
                    if cooldown >= 60:  # if the cooldown is more than or equal to 60
                        m = cooldown // 60  # easy here.
                        msg += f"{m} minute"  # I commented enough for easy understanding from here/
                        if m % 10 != 1:
                            msg += 's'
                        msg += ", "
                    s = cooldown // 60
                    msg += f"{s} second"
                    if s % 10 != 1:
                        msg += 's'
                    return await ctx.send(msg + " until you can appeal again.")

        channel = self.bot.get_channel(self.channel_id)  # gets channel id from `self.channel_id`
        try:  # easy, very easy to guess 
            ban_entry = await channel.guild.fetch_ban(ctx.author)  # fetches the ban from the channel's server
        except discord.errors.NotFound:  # if there is not a ban for that user
            return await ctx.send("You\'re not banned :D")  # say 'You\'re not banned'

        e = discord.Embed(color=utils.theme_color(ctx.bot))  # define the embed
        e.description = "Appeals need to contain why you are banned, and a reason " \  # create a description
                        "for being unbanned. Lack of either, or abuse of this command results " \  # backslash continues it.
                        "in not being able to use the command anymore!"
        for text_group in [appeal[i:i + 1000] for i in range(0, len(appeal), 1000)]:  # I really can not be bothered to explain this.
            e.add_field(name='◈ Your Appeal', value=text_group, inline=False)  # add a field saying what is in `name=*` and value `value=*`
        e.set_footer(text='React to accept/deny')  # set the footer
        msg = await ctx.send(embed=e)  # send the message
        await msg.add_reaction('👍')  # add thumbs up emoji
        await msg.add_reaction('👎')  # add a thumbs down emoji

        def pred(r, u):  # explained in the docstring below
            """ assure the conditions of the reaction is in the right location """
            return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id  # easy return.

        try:  
            reaction, user = await self.bot.wait_for('reaction_add', check=pred, timeout=360)  # wait for a reaction added
        except asyncio.TimeoutError:  # if there is a timeout error
            return await msg.edit(content='This menu has expired', embed=e)
        if str(reaction.emoji) == '👍':  # easy to read now.
            e = discord.Embed(color=ctx.author.color)
            e.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            if isinstance(ctx.guild, discord.Guild):
                e.set_thumbnail(url=ctx.guild.icon_url)
            e.description = appeal
            e.add_field(name='◈ Logged Ban Reason', value=str(ban_entry.reason))
            e.set_footer(text=str(ctx.author.id))
            appeal = await channel.send(embed=e)
            await appeal.add_reaction('👍')
            await appeal.add_reaction('👎')
            await appeal.add_reaction('🛑')
            await ctx.send('Sent your appeal request to CT')
            self.blacklist[user_id] = {
                'cooldown': time() + 60 * 60 * 2,
                'banned': False
            }
            self.save_data()
        elif str(reaction.emoji) == '👎':
            await ctx.send("Alright, feel free to resubmit with the correct parameters")
        else:
            await msg.clear_reaction(reaction.emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):  # on a reaction added.
        if payload.channel_id == self.channel_id:
            channel = self.bot.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            user = channel.guild.get_member(payload.user_id)
            if user.bot:
                return
            if not user.guild_permissions.administrator:
                return await msg.remove_reaction(payload.emoji, user)
            target_id = msg.embeds[0].footer.text
            target = self.bot.get_user(int(target_id))
            emoji = str(payload.emoji)
            if emoji == '👍':
                await channel.guild.unban(target, reason=f"Appeal by {user}")
                await msg.edit(content=f"Unbanned by {user}", embed=msg.embeds[0])
                try:
                    await target.send("Your appeal request was accepted")
                except discord.errors.Forbidden:
                    pass
            elif emoji == '👎':
                await msg.edit(content=f"Appeal rejected by {user}", embed=msg.embeds[0])
                await msg.clear_reactions()
                self.blacklist[target_id] = {
                    'cooldown': time() + 60 * 60 * 24 * 2,
                    'banned': False
                }
                self.save_data()
                try:
                    await target.send("Your ban appeal was denied, you can retry in 2 days")
                except discord.errors.Forbidden:
                    pass
            elif emoji == '🛑':
                await msg.edit(content=f"Banned from appeals by {user}", embed=msg.embeds[0])
                await msg.clear_reactions()
                self.blacklist[target_id] = {
                    'cooldown': None,
                    'banned': True
                }
                self.save_data()
                try:
                    await target.send("Your ban appeal was rejected an you've been banned from ban appeals")
                except discord.errors.Forbidden:
                    pass
            else:
                await msg.clear_reaction(payload.emoji)


def setup(bot):
    bot.add_cog(Appeals(bot))
