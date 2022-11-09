from discord.ext import commands
from serverstatus import ServerStatus


class ServerOperation(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        # self.mc_channel_id = 877587539991605290
        # test
        self.mc_channel_id = 965978774963359817

    async def changeStatus(self, ststus):
        self.bot.server_status = ststus

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


def setup(bot):
    return bot.add_cog(ServerOperation(bot=bot))
