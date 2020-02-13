from discord.ext import commands
import cleverbotfree.cbfree
import sys
cb = cleverbotfree.cbfree.Cleverbot()

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @client.event()
    @commands.command(description="Enter chat")
    async def chat(ctx):
        try:
            cb.browser.get(cb.url)
        except:
            cb.browser.close()
            sys.exit()
        while True:
            try:
                cb.get_form()
            except:
                sys.exit()
            msg = await client.wait_for('message', check=check)
            userInput = msg.content
            if userInput == 'quit':
                break
            cb.send_input(userInput)
            resp = cb.get_response()
            ctx.send(resp)
        cb.browserr.close()

def setup(bot):
    bot.add_cog(Chat(bot))
