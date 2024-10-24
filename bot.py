import discord
from discord.ext import commands
from datetime import datetime
import json
import logging
from pathlib import Path

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="^", intents=intents, help_command=None)

# Load Google API key from api_keys.json
with open('api_keys.json', 'r') as api_keys_file:
    api_keys_data = json.load(api_keys_file)
    google_api_key = api_keys_data.get('google_api_key')

# Load bot TOKEN from config.json (must be loaded before running the bot)
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)
    bot_token = config_data.get('token')

# Set up logging configuration
log_folder = "Logs"
current_month_year = datetime.now().strftime("%B %Y")
log_folder_path = Path(log_folder) / current_month_year
log_folder_path.mkdir(parents=True, exist_ok=True)

# Configure log file path
log_file_path = log_folder_path / f"{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(filename=log_file_path, level=logging.INFO)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    cogs = {
        "Moderation": [
            "cogs.moderation.kick",
            "cogs.moderation.ban",
            "cogs.moderation.timeout",
            "cogs.moderation.rename"
        ],
        "Fun": [
            "cogs.fun.eightball",
            "cogs.fun.dog"
        ],
        "Resources": [
            "cogs.resources.resume_guide",
            "cogs.resources.templates",
            "cogs.resources.blog",
            "cogs.resources.forfoxsake",
            "cogs.resources.five_pillars"
        ],
        "Technical": [
            "cogs.technical.url_checker",
            "cogs.technical.crack"
        ],
        "General": [
            "cogs.general.hello",
            "cogs.general.help",
            "cogs.general.time",
            "cogs.general.poll",
            "cogs.general.translate",
            "cogs.general.role_info"
        ]
    }

    for category, cogs_list in cogs.items():
        for cog in cogs_list:
            try:
                await bot.load_extension(cog)
                print(f"{category} cog loaded successfully.")
            except Exception as e:
                print(f"Failed to load {cog}: {e}")
    
# Log commands and responses
@bot.event
async def on_command(ctx):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    command_log = f"[{timestamp}] Command Received: {ctx.message.content}"
    print(command_log)  # Output to console
    logging.info(command_log)  # Log to file

@bot.event
async def on_command_completion(ctx):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response_log = f"[{timestamp}] Response Sent: {ctx.message.content} -> {ctx.message.clean_content}"
    print(response_log)  # Output to console
    logging.info(response_log)  # Log to file

# Error handler to catch permission errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the required permissions to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing argument: {error.param}")
    else:
        await ctx.send(f"An error occurred: {error}")

# Bot Token
bot.run(bot_token)
