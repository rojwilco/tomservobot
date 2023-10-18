import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord with intents {[intent for intent in intents]}')
    print(f'{client.user} is connected to the following servers:')
    for guild in client.guilds:
        print(f'- {guild.name} ({guild.id})')

@client.event
async def on_message(message):
    print(f'processing message: {message.content}')
    # don't respond to myself
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello there!!')


client.run(TOKEN)
