from discord import Guild, Member, Role
from discord.ext import commands, tasks
from discord.ext.commands import Context

from MCServerBot import MCServerBot

import random

class Debug(commands.Cog):
    def __init__(self, bot : MCServerBot) -> None:
        super().__init__()
        self.bot : MCServerBot = bot
        self.server_admin_id : int = 851408507194572821
        self.mc_channel = self.bot.get_channel(965978774963359817)
        self.guild : Guild = self.bot.get_guild(965978774963359814)
        self.server_admin_roll : Role = self.guild.get_role(1040592221264683099)
        
        self.stopable = False
        self.demoProcess = None
        self.nlogin = 0
    
    @commands.command()
    async def logDebug(self, context : Context):
        if self.bot.server.process is None:
            return
        print(self.bot.server.getJoinLog())
        print(self.bot.server.getJoinNumber())

    @commands.command()
    async def debug(self, context : Context):
        user = context.message.author
        if(type(user) is not Member):
            print(type(user))
            return
        
        await context.send("you are admin!!")
        if self.periodicallyStop.is_running():
            await context.send("stop loop @851408507194572821", mention_author=True)
            self.periodicallyStop.cancel()
        else:
            await context.send("start loop")
            await self.mc_channel.send("stop after 30 minutes if no one is logged in")
            self.periodicallyStop.start()
            if(0):
                await context.send("0 is True")
            else:
                await context.send("0 is False")
                
    async def demoStop(self):
        await self.mc_channel.send("demo stop")
        self.demoProcess = None
        
    def demoJoinNumber(self):
        return random.randint(0,2)

    def checkAnyoneJoined(self) -> bool:
        rand = self.demoJoinNumber()
        print(rand)
        if 0 == rand:
            return False
        
        return True
    
    @tasks.loop(seconds=5)
    async def periodicallyStop(self):
        print(self.stopable)
        if self.checkAnyoneJoined():
            # debug
            if self.stopable:
                await self.mc_channel.send("while loop anyone login")
            else:
                await self.mc_channel.send("playing")
                
            self.stopable = False
            return
        
        if self.stopable:
            await self.mc_channel.send("periodically stop")
            await self.demoStop()
            self.stopable = False
            self.periodicallyStop.cancel()
            return
        
        self.stopable = True
        await self.mc_channel.send("next loop will stop")        
        
    @periodicallyStop.before_loop
    async def before_periodicallyStop(self):
        await self.bot.wait_until_ready()

def setup(bot):
    return bot.add_cog(Debug(bot=bot))
