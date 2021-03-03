import discord
import logging
import json

from discord.ext import commands

from harptos_calendar import Calendar
from weather import *

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
@commands.has_permissions(administrator=True)
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
async def moon(ctx, *, days=None):
    if not days:
        days = calendar.current_day
    message = calendar.string_moon(calendar.current_moons(days))
    await ctx.send(message)

@client.command()
async def month(ctx):
    month = calendar.current_month
    name = month.get("name")
    alternative = month.get("alternative")
    sign = month.get("sign")
    holidays = month.get("holidays")
    days = month.get("days")
    message = f"It is now the {name}{' also known as ' + alternative if alternative else ''}.\n"
    message += f"The {'day' if days == 1 else 'month'} is dedicated to the Sign of the {sign.title()}.\n"
    if days == 1:
        message += "The holiday is celebrated in most regions"
    else:
        message += f"The month has {days} days and has "
        if holidays:
            if len(holidays) == 1:
                message += "one major celebration.\n"
            else:
                message += f"{len(holidays)} major celebrations.\n"
        else:
            message += "no major celebrations.\n"
    if holidays:
        message += "**Celebrations**:\n"
        for key, value in holidays.items():
            message += f"{key} - Day {value}"
    await ctx.send(message)

@client.command()
async def howlong(ctx):
    await ctx.send(f"It has been {calendar.days_since_start()} days since your adventure began.")

@client.command()
async def holiday(ctx):
    days, holiday = calendar.closest_holiday()
    if days == 0:
        await ctx.send(f"Today is the **{holiday.get('name')}**!")
    else:
        await ctx.send(f"The closest holiday is the **{holiday.get('name')}** in {days} days")

### weather

@client.command()
@commands.has_permissions(administrator=True)
async def weather(ctx, *, days=0):
    # check if already generated
    message = weather_records.get(str(calendar.current_day + days), None)
    if message:
        message = message.get("forecast")
    else:
        message = DailyForecast(calendar.current_day + days, calendar.day_of_year + days).forecast_string
    await ctx.send(message)

client.run(token)