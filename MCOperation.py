from discord.ext import commands
from serverstatus import ServerStatus


class ServerOperation(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    async def changeStatus(self, ststus):
        self.bot.server_status = ststus

    @commands.command()
    async def start(self, context):
        if self.bot.server_status not in self.bot.allowed:
            return
        # await context.send(context.channel.id)
        channel = self.bot.get_channel(965978774963359817)
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
            await self.changeStatus(ServerStatus.waiting)
        else:
            await self.changeStatus(ServerStatus.stop)

    @commands.command()
    async def stop(self, context):
        if self.bot.server_status not in self.bot.allowed:
            return
        channel = self.bot.get_channel(965978774963359817)
        if context.channel is not channel:
            return

        await context.send("stop")
        await self.changeStatus(ServerStatus.stopping)
        for log in self.bot.server.stop():
            print(log)

        await self.changeStatus(ServerStatus.stop)


def setup(bot):
    return bot.add_cog(ServerOperation(bot=bot))
