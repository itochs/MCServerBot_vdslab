from discord.ext import commands
from serverstatus import ServerStatus
from server import Server


class MCServerBot(commands.Bot):

    def __init__(self, command_prefix, intents, jar_directory_path):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.server = Server()
        self.server_status = ServerStatus.stop
        self.jar_directory_path = jar_directory_path
        self.allowed = [ServerStatus.stop,
                        ServerStatus.playing,
                        ServerStatus.waiting]
        self.COGs = ["MCOperation"]

    async def on_ready(self):
        print("=====")
        print("login")
        print("=====")
        for cog in self.COGs:
            await self.load_extension(cog)
