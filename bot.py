import discord
import logging
import json

from discord.ext import commands

# setup logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
    )

# get bot token
with open('token.txt', 'r') as reader:
    token = reader.read()
    logging.info("Token Retrieved")

# import settings
with open("settings.json") as json_file:
    settings = json.load(json_file)
    logging.info("Settings Retrieved")

# setup command prefix
client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    """Run on Start"""
    logging.info("Bot is Ready")


client.run(token)