""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

from discord.ext import commands
from discord.ext.commands import Context


# Here we name the cog and create a new class for the cog.
class Article(commands.Cog, name="article"):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="summarize",
        description="Summarizes an article",
    )
    async def summarize(self, context: Context, url: str) -> None:
        """
        Summarizes an article 

        :param context: The application command context.
        :param url: URL to the article to summarize
        """
        # Do your stuff here

        # Don't forget to remove "pass", I added this just because there's no content in the method.
        await context.send(f"Sure I'll summarize {url} for you champ")


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Article(bot))
