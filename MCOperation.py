from discord import Member
from discord import Guild
from discord import Role
from discord.ext import commands
from discord.ext.commands import Bot
from serverstatus import ServerStatus
from MCServerBot import MCServerBot


class ServerOperation(commands.Cog):
    def __init__(self, bot : MCServerBot) -> None:
        super().__init__()
        self.bot : MCServerBot = bot
        if __debug__:
            self.mc_channel_id : int = 965978774963359817
            self.guild : Guild = self.bot.get_guild(965978774963359814)
        else:
            self.mc_channel_id : int = 877587539991605290
            self.guild : Guild  = self.bot.get_guild(730627809709391943)
        
        self.server_admin_roll : Role = self.guild.get_role(806539400984920114)
        self.server_admin_id : int = 851408507194572821

    async def changeStatus(self, ststus : ServerStatus):
        self.bot.server_status : ServerStatus = ststus

    @commands.command()
    async def start(self, context):
        if self.bot.server_status not in self.bot.allowed:
            return
        # await context.send(context.channel.id)
        channel = self.bot.get_channel(self.mc_channel_id)
        if context.channel is not channel:
            return

        await context.send("starting......")
        await self.changeStatus(ServerStatus.starting)

        startable = True
        for log in self.bot.server.start(self.bot.jar_directory_path):
            print(log)
            if "error" in log:
                startable = False

        if startable:
            await context.send("start!!!")
            await self.changeStatus(ServerStatus.waiting)
        else:
            await context.send("failed starting... Sorry @851408507194572821")
            await self.changeStatus(ServerStatus.stop)

    @commands.command()
    async def stop(self, context):
        if self.bot.server_status not in self.bot.allowed:
            return
        channel = self.bot.get_channel(self.mc_channel_id)
        if context.channel is not channel:
            return

        await context.send("stopping...")
        await self.changeStatus(ServerStatus.stopping)
        for log in self.bot.server.stop():
            print(log)

        await self.changeStatus(ServerStatus.stop)
        await context.send("stop!!")
    
    @commands.command()
    async def debug(self, context):
        # test
        user = context.message.author
        if(type(user) is not Member):
            print(type(user))
            return
        user : Member
        user_role  = user.get_role(1040592221264683099)
        user_has_admin_role = user_role and user_role is not self.guild.get_role(1040592221264683099)
        if user_has_admin_role:
            print("not admin")
        
        print("admin")


def setup(bot):
    return bot.add_cog(ServerOperation(bot=bot))
