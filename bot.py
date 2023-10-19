import asyncio
import os

from discord import (
    Intents
)
from discord.ext import commands
from dotenv import load_dotenv

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx, *, member = None):
        """Says hello"""
        member = member or ctx.author
        await ctx.send(f'Well, hey there, {member.name}!')


async def main():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    intents = Intents.default()
    intents.typing = False
    intents.presences = False
    intents.message_content = True

    bot = commands.Bot(command_prefix="$", intents=intents)
    print(f'Loading Cogs...')
    await bot.add_cog(Greetings(bot))

    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord with intents {[intent for intent in intents]}')
        print(f'{bot.user} is connected to the following servers:')
        for guild in bot.guilds:
            print(f'- {guild.name} ({guild.id})')

    # @bot.event
    # async def on_message(message):
    #     print(f'processing message: {message.content}')
    #     # don't respond to myself
    #     if message.author == bot.user:
    #         return

    #     if message.content.startswith('$hello2'):
    #         await message.channel.send('Hello there!!')



    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())