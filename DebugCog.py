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
        user : Member
        user_role  = user.get_role(1040592221264683099)
        user_has_admin_role = user_role and user_role is self.server_admin_roll
        user_is_admin = user.id == self.server_admin_id
        if not user_has_admin_role and not user_is_admin:
            await context.send("you are not admin")
            return
        
        await context.send("you are admin!!")
        if self.loopDebug.is_running():
            await context.send("stop loop @851408507194572821")
            self.loopDebug.cancel()
        else:
            await context.send("start loop")
            self.demoProcess = "demo"
            if(0):
                await context.send("0 is True")
            else:
                await context.send("0 is False")
            self.loopDebug.start()
                
    async def demoStop(self):
        await self.mc_channel.send("demo stop")
        self.demoProcess = None
        
    def demoJoinNumber(self):
        return random.randint(0,2)
    
    @tasks.loop(seconds=3)
    async def loopDebug(self):
        joinNumber = self.demoJoinNumber()
        await self.mc_channel.send(f"loop: n -> {joinNumber}, stopable {self.stopable}")
        if self.stopable:
            self.stopable = False
            if joinNumber == 0:
                await self.mc_channel.send("demo stop")
                await self.demoStop()
                self.loopDebug.cancel()
        else:
            if joinNumber == 0:
                await self.mc_channel.send("demo stop after 30 minutes if no one is logged in")
                self.stopable = True

def setup(bot):
    return bot.add_cog(Debug(bot=bot))
