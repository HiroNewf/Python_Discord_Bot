import discord
from discord.ext import commands
import asyncio

# Help pages
help_pages = [
    ("### General Commands\n"
     "- `^help`: A general help command that lists out all of the commands the bot supports and provides general usage information as well as command examples.\n"
     "- `^hello`: A greeting/testing command. This command should just respond with 'Hello!' and is mainly just used as a sort of ping command to make sure the bot is up.\n"
     "- `^time`: Displays the time and allows for an optional timezone argument that supports a variety of timezone formats (ETC, UTC+04:00, America/New_York).\n"
     "  - Examples:\n"
     "    - `^time JST`\n"
     "    - `^time UTC-06:00`\n"
     "    - `^time Asia/Shanghai`\n"
     "- `^settimezone [timezone]`: Sets the timezone for the user running the command.\n"
     "  - Example: `^settimezone America/Anchorage`\n"
          "- `^poll [question] [options...]`: Creates a poll with the given question and options. You can provide up to 9 options.\n"
     "  - Example: `^poll What's your favorite color? Red Blue Green`\n"
     "- `^translate [language] [text]`: Translates the provided text into the specified language.\n"
     "  - Example: `^translate es Hello, world!`\n"
     "- `^role_info [role_name]`: Provides information about a specific role, including members who have that role.\n"
     "  - Example: `^role_info Admin`\n"),
     
     ("### Fun Commands\n"
     "- `^8ball [question]`: Ask the magic 8-ball a question and receive an answer.\n"
     "  - Example: `^8ball Will it rain today?`\n"
     "- `^dog`: Gives you a random picture of a dog.\n"),
     
    ("### Technical Commands\n"
     "- `^crack [hash]`: Identifies the hash type provided and attempts to crack the hash with the rockyou.txt wordlist.\n"
     "  - Example: `^crack 68e109f0f40ca72a15e05cc22786f8e6`\n"
     "- `^URL_Checker [URL]`: Runs the provided URL against Google's Safe Browsing database.\n"
     "  - Example: `^URL_Checker https://google.com`\n"),
     
    ("### Resource Links\n"
    "- `^resumeguide`: Provides the link to Hiro's resume guide.\n"
    "- `^templates`: Provides the link Hiro's resume templates and examples.\n"
    "- `^blog`: Provides the link to Hiro's blog.\n"
    "- `^forfoxsake`: Provides the link to Erubius's website & blog.\n"
    "- `^fivepillars`: Provides the link to the fivepillars github page.\n"),
    
    ("### Moderation Commands\n"
     "- `^kick @user [reason]`: Kicks a user from the server with an optional reason.\n"
     "- `^ban @user [reason]`: Bans a user from the server with an optional reason.\n"
     "- `^timeout @user [time in seconds] [reason]`: Temporarily mutes a user for a specified amount of time.\n"
     "- `^rename @user [new nickname]`: Renames a user to the specified nickname on the server.\n")
]

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def custom_help(self, ctx):
        page = 0
        total_pages = len(help_pages)

        embed = discord.Embed(title="Help Command", description=help_pages[page], color=discord.Color.blue())
        embed.set_footer(text=f"Page {page + 1}/{total_pages}")
        message = await ctx.send(embed=embed)

        # Adding the navigation reactions
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"]

        while True:
            try:
                # Wait for a reaction from the user
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)

                if str(reaction.emoji) == "➡️":
                    # Next page
                    page += 1
                    if page >= total_pages:
                        page = 0  # Loop around to the first page

                elif str(reaction.emoji) == "⬅️":
                    # Previous page
                    page -= 1
                    if page < 0:
                        page = total_pages - 1  # Loop around to the last page

                # Update the embed with the new page
                embed = discord.Embed(title="Help Command", description=help_pages[page], color=discord.Color.blue())
                embed.set_footer(text=f"Page {page + 1}/{total_pages}")
                await message.edit(embed=embed)

                # Remove the user's reaction so they can react again
                await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                # After 60 seconds of inactivity, clear reactions and end the loop
                await message.clear_reactions()
                break

async def setup(bot):
    await bot.add_cog(Help(bot))
