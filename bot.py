import discord
import logging
import json

from discord.ext import commands

from harptos_calendar import Calendar

calendar = Calendar()

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

@client.command()
async def today(ctx):
    year, day = calendar.current_date(calendar.current_day)
    logging.info("Sending current date")
    await ctx.send(f"Year {calendar.start_year + year}, {day}")

@client.command()
async def days(ctx, *, days):
    try:
        days = int(days)
    except:
        logging.info("Non int passed")
        await ctx.send(f"Sorry, could not understand '{days}'")
    calendar.add_days(days)
    logging.info("Days added successfully")
    await ctx.send("Current date changed!")

client.run(token)