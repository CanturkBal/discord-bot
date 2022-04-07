
from discord.ext import commands
import discord
from datetime import datetime
class Mycog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_message(self,msg):
        if msg.content == "hello":
            await msg.channel.send("HI!")        
    @commands.command()
    async def black(self,context):
        await context.send("white")
    

def setup(bot):
    bot.add_cog(Mycog(bot))
