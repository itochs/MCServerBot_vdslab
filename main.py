import os
import discord
from mcserverbot import MCServerBot
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
server_bot = mcserverbot.MCServerBot(command_prefix='!', intents=intents)
server_bot.run(os.getenv("TOKEN"))
