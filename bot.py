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
    message = calendar.today_as_str()
    logging.info("Sending current date")
    await ctx.send(message)

@client.command()
async def days(ctx, *, days):
    try:
        days = int(days)
    except:
        logging.info("Non int passed")
        await ctx.send(f"Sorry, could not understand '{days}'")
    calendar.add_days(days)
    logging.info("Days added successfully")
    await ctx.send(f"Current date changed!\n {calendar.today_as_str()}")

@client.command()
async def moon(ctx, *, days=calendar.current_day):
    message = calendar.string_moon(calendar.current_moons(days))
    await ctx.send(message)

# @client.command()
# async def clear(ctx, amount=10):
#     await ctx.channel.purge(limit=amount)

client.run(token)