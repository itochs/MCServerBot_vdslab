#!/usr/bin/env -S python -O
import os

import discord

from MCServerBot import MCServerBot

if __debug__:
    from dotenv import load_dotenv
    load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
jar_dir_path = os.getenv("JAR_DIR_PATH")
bot_token = None
if __debug__:
    bot_token = os.getenv("BOT_TEST_TOKEN")
# else:

if jar_dir_path is None:
    exit("jar directory path is none")

if bot_token is None:
    exit("env error. bot token is none")

print(jar_dir_path)
server_bot = MCServerBot(
    command_prefix='!',
    intents=intents,
    jar_directory_path=jar_dir_path)
server_bot.run(bot_token)
