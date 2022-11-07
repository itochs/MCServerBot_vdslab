import os
import discord
from MCServerBot import MCServerBot
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
jar_dir_path = os.getenv("JAR_DIR_PATH")
print(jar_dir_path)
server_bot = MCServerBot(
    command_prefix='!', intents=intents, jar_directory_path=jar_dir_path)
server_bot.run(os.getenv("TEST_TOKEN"))
