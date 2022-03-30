import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext import tasks
import asyncio
import os
import random
import urllib
import json

# Get the Bot's token
load_dotenv()
token = str(os.getenv('KUNTOKEN'))

# Set the bot's command prefix
prefix = "k- "
client = commands.Bot(command_prefix=f'{prefix}', help_command=None)

# Loop through the different activities "playing" for the bot's activity status 
@tasks.loop(seconds=20.0)
async def my_background_task():
    philosophers = ['Kongzi','Xunzi','Lord Shang','Han Feizi','Laozi','Mozi']
    philosopher = random.choice(philosophers)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'{prefix}help'))
    await asyncio.sleep(10)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'Vibing with {philosopher}'))

# Ready message 
@client.event
async def on_ready():
    print("Kun is up and running ~")
    await client.wait_until_ready()
    my_background_task.start()

# Load all cogs 
client.load_extension('cogs.samples')
client.load_extension('cogs.practice')

client.run(token)