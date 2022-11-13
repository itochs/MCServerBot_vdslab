from discord import Guild, Member, Role, TextChannel
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

from MCServerBot import MCServerBot
from serverstatus import ServerStatus


class ServerOperation(commands.Cog):
    def __init__(self, bot : MCServerBot) -> None:
        super().__init__()
        self.bot : MCServerBot = bot
        self.server_admin_id : int = 851408507194572821
        self.stopable = False

        # vdslab
        self.mc_channel = self.bot.get_channel(877587539991605290)
        self.guild = self.bot.get_guild(730627809709391943)
        self.server_admin_roll_id = 806539400984920114
        if self.guild:
            self.server_admin_roll = self.guild.get_role(self.server_admin_roll_id)
        
        # private channel
        if __debug__:
            self.mc_channel = self.bot.get_channel(965978774963359817)
            self.guild = self.bot.get_guild(965978774963359814)
            self.server_admin_roll_id = 1040592221264683099
            if self.guild:
                self.server_admin_roll = self.guild.get_role(self.server_admin_roll_id)
            

    async def __changeStatus(self, ststus : ServerStatus):
        self.bot.server_status : ServerStatus = ststus

    @commands.command()
    async def start(self, context : Context):
        if self.bot.server_status not in self.bot.allowed:
            return
        if context.channel is not self.mc_channel:
            return

        await context.send("starting......")
        await self.__changeStatus(ServerStatus.starting)

        startable = True
        for log in self.bot.server.start(self.bot.jar_directory_path):
            print(log)
            if "error" in log:
                startable = False

        if startable:
            await context.send("started!!!")
            await self.__changeStatus(ServerStatus.waiting)
        else:
            await context.send("failed starting... Sorry @851408507194572821")
            await self.__changeStatus(ServerStatus.stop)

    async def __stopProcess(self):
        await self.mc_channel.send("stopping...")
        await self.__changeStatus(ServerStatus.stopping)
        for log in self.bot.server.stop():
            print(log)

        await self.__changeStatus(ServerStatus.stop)
        await self.mc_channel.send("stopped!!")
    
    @commands.command()
    async def stop(self, context : Context):
        if self.bot.server_status not in self.bot.allowed:
            return
        if context.channel is not self.mc_channel:
            return
        if not self.stopable:
            return
        
        user = context.message.author
        if(type(user) is not Member):
            await context.send("User could not verify. sorry :(")
            return
        
        user_role  = user.get_role(self.server_admin_roll_id)
        user_has_admin_role = user_role and user_role is self.server_admin_roll
        user_is_admin = user.id == self.server_admin_id
        
        if not user_has_admin_role and not user_is_admin:
            await context.send("You are not admin? Only admin can stop")
            return

        await self.__stopProcess()
    
    @tasks.loop(minutes=30)
    async def periodicallyStop(self):
        joinNumber = self.bot.server.getJoinNumber()
        if self.stopable:
            if joinNumber == 0:
                await self.mc_channel.send("periodically stop")
                await self.__stopProcess()
                self.periodicallyStop.cancel()

            self.stopable = False
        else:
            if joinNumber == 0:
                await self.mc_channel.send("stop after 30 minutes if no one is logged in")
                self.stopable = True
    
def setup(bot):
    return bot.add_cog(ServerOperation(bot=bot))
