from discord.ext import commands

from server import Server
from serverstatus import ServerStatus


class MCServerBot(commands.Bot):

    def __init__(self, command_prefix, intents, jar_directory_path):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.server : Server = Server()
        self.server_status : ServerStatus = ServerStatus.stop
        self.jar_directory_path : str= jar_directory_path
        self.allowed : list = [ServerStatus.stop,
                        ServerStatus.playing,
                        ServerStatus.waiting]
        self.COGs = ["MCOperation"]
        if __debug__:
            self.COGs = ["MCOperation", "DebugCog"]

    async def on_ready(self):
        print("=====")
        print("login")
        print("=====")
        for cog in self.COGs:
            await self.load_extension(cog)
