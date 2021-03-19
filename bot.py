import discord
import logging
import json

from discord.ext import commands

from database import Guild, session
from harptos_calendar import Calendar
from weather import *

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
with open('data/token.txt', 'r') as reader:
    token = reader.read()
    logging.info("Token Retrieved")

# setup command prefix
client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    """Run on Start"""
    logging.info("Bot is Ready")
    # for guild in client.guilds:
    #     logging.info(guild.id)
    # create DB for existing guilds
    # for guild in client.guilds:
    #     guild = Guild(guild.id)
    #     session.add(guild)
    #     session.commit()
    # for i in session.query(Guild).all():
    #     logging.info(guild.guild)

@client.command()
async def today(ctx):
    """Get the current date."""
    calendar = Calendar(ctx.guild.id)
    message = f"Today is the {calendar.day_as_str()}"
    await ctx.send(message)

@client.command()
async def firstday(ctx):
    """Get the current date."""
    calendar = Calendar(ctx.guild.id)
    message = f"The adventure started on the {calendar.day_as_str(calendar.first_day, False)}"
    await ctx.send(message)

@client.command()
async def moon(ctx, *, days=0):
    """Get the current moon phase."""
    calendar = Calendar(ctx.guild.id)
    days = calendar.current_day + int(days)
    message = calendar.string_moon(calendar.current_moons(days))
    await ctx.send(message)

############### Admin commands ###############
@client.command()
@commands.has_permissions(administrator=True)
async def days(ctx, *, days):
    """Change current day by n. n can be positive/negative."""
    try:
        days = int(days)
    except:
        logging.info("Non int passed")
        await ctx.send(f"Sorry, please provide valid integers")
    calendar = Calendar(ctx.guild.id)
    calendar.add_days(days)
    logging.info("Current Day changed successfully")
    await ctx.send(f"Current date changed!\n Today is the {calendar.day_as_str()}")

@client.command()
@commands.has_permissions(administrator=True)
async def startday(ctx, *, days):
    """Change first day by n. n can be positive/negative."""
    try:
        days = int(days)
    except:
        logging.info("Non int passed")
        await ctx.send(f"Sorry, please provide valid integers")
    calendar = Calendar(ctx.guild.id)
    calendar.add_days(days, "first_day")
    logging.info("Start Day changed successfully")
    await ctx.send(f"Start date changed to:\n {calendar.day_as_str(calendar.first_day, False)}")



# @client.command()
# async def month(ctx):
#     month = calendar.current_month
#     name = month.get("name")
#     alternative = month.get("alternative")
#     sign = month.get("sign")
#     holidays = month.get("holidays")
#     days = month.get("days")
#     message = f"It is now the {name}{' also known as ' + alternative if alternative else ''}.\n"
#     message += f"The {'day' if days == 1 else 'month'} is dedicated to the Sign of the {sign.title()}.\n"
#     if days == 1:
#         message += "The holiday is celebrated in most regions"
#     else:
#         message += f"The month has {days} days and has "
#         if holidays:
#             if len(holidays) == 1:
#                 message += "one major celebration.\n"
#             else:
#                 message += f"{len(holidays)} major celebrations.\n"
#         else:
#             message += "no major celebrations.\n"
#     if holidays:
#         message += "**Celebrations**:\n"
#         for key, value in holidays.items():
#             message += f"{key} - Day {value}"
#     await ctx.send(message)

@client.command()
async def howlong(ctx):
    calendar = Calendar(ctx.guild.id)
    await ctx.send(f"It has been {calendar.days_since_start()} days since your adventure began.")

# @client.command()
# async def holiday(ctx):
#     days, holiday = calendar.closest_holiday()
#     if days == 0:
#         await ctx.send(f"Today is the **{holiday.get('name')}**!")
#     else:
#         await ctx.send(f"The closest holiday is the **{holiday.get('name')}** in {days} days")

# ### weather

# @client.command()
# @commands.has_permissions(administrator=True)
# async def weather(ctx, *, days=0):
#     # check if already generated
#     message = weather_records.get(str(calendar.current_day + days), None)
#     if message:
#         message = message.get("forecast")
#     else:
#         message = DailyForecast(calendar.current_day + days, calendar.day_of_year + days).forecast_string
#     await ctx.send(message)

client.run(token)

