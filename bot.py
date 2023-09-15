import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')
    print(f'{client.user} is connected to the following servers:')
    for guild in client.guilds:
        print(f'- {guild.name} ({guild.id})')

client.run(TOKEN)
