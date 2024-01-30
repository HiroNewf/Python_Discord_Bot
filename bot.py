import discord
from discord.ext import commands
import re
import asyncio
from datetime import datetime, timezone
import pytz
import hashlib
import bcrypt
import json
import requests
import logging
import os
import random
from pathlib import Path

intents = discord.Intents.all()

# Set up logging configuration
log_folder = "Logs"
current_month_year = datetime.now().strftime("%B %Y")
log_folder_path = Path(log_folder) / current_month_year
log_folder_path.mkdir(parents=True, exist_ok=True)

# Configure log file path
log_file_path = log_folder_path / f"{datetime.now().strftime('%Y-%m-%d')}.log"

logging.basicConfig(filename=log_file_path, level=logging.INFO)

bot = commands.Bot(command_prefix="^", intents=intents, help_command=None)

rockyou_path = 'rockyou.txt'
timezones_file = 'user_timezones.json'
advanced_commands_enabled = False

# Load bot TOKEN from config.json
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)
    bot_token = config_data.get('token')

# Load Google API key from api_keys.json
with open('api_keys.json', 'r') as api_keys_file:
    api_keys_data = json.load(api_keys_file)
    google_api_key = api_keys_data.get('google_api_key')
    hibp_api_key = api_keys_data.get('hibp_api_key')

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
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

# Command: Hello
@bot.command(name='hello')
async def hello(ctx):
    """Greeting / Testing Command"""
    await ctx.send('Hello!')

# Command: Crack
@bot.command(name='crack')
async def identify_hash(ctx, hash_input):
    """
    Identifies the hash type and attempts to crack the password with rockyou.txt

    Example command: ^crack 68e109f0f40ca72a15e05cc22786f8e6
    """
    async with ctx.typing():
        result = await crack_password(hash_input)
    await ctx.send(result)

async def crack_password(hash_input):
    """
    Attempts to crack the password for a given hash with rockyou.txt

    Example command: ^crack 68e109f0f40ca72a15e05cc22786f8e6
    """
    # Hash formats for identification
    hash_formats = {
        'MD5': re.compile(r'^[0-9a-fA-F]{32}$'),
        'SHA-1': re.compile(r'^[0-9a-fA-F]{40}$'),
        'SHA-256': re.compile(r'^[0-9a-fA-F]{64}$'),
        'SHA-512': re.compile(r'^[0-9a-fA-F]{128}$'),
        'bcrypt': re.compile(r'^\$2[aby]\$[0-9]+\$[0-9a-zA-Z./]+'),
        'NTLM': re.compile(r'^[0-9a-fA-F]{32}:[0-9a-fA-F]{32}$'),
        'LM': re.compile(r'^[0-9a-fA-F]{16}$'),
        'RipeMD-160': re.compile(r'^[0-9a-fA-F]{40}$'),
        'Whirlpool': re.compile(r'^[0-9a-fA-F]{128}$'),
        'Tiger-160': re.compile(r'^[0-9a-fA-F]{40}$'),
        'GOST R 34.11-94': re.compile(r'^[0-9a-fA-F]{64}$'),
        'CRC32': re.compile(r'^[0-9a-fA-F]{8}$'),
        'LMv2': re.compile(r'^[0-9a-fA-F]{48}$'),
        'Snefru-256': re.compile(r'^[0-9a-fA-F]{64}$'),
        'SHA-224': re.compile(r'^[0-9a-fA-F]{56}$'),
        'Haval-256,3': re.compile(r'^[0-9a-fA-F]{64}$'),
        'Snefru-128': re.compile(r'^[0-9a-fA-F]{32}$'),
        'SHA3-224': re.compile(r'^[0-9a-fA-F]{56}$'),
        'SHA3-256': re.compile(r'^[0-9a-fA-F]{64}$'),
        'SHA3-384': re.compile(r'^[0-9a-fA-F]{96}$'),
        'SHA3-512': re.compile(r'^[0-9a-fA-F]{128}$'),
        'Tiger-128,3': re.compile(r'^[0-9a-fA-F]{32}$'),
        'Haval-224,3': re.compile(r'^[0-9a-fA-F]{56}$'),
        'GOST CryptoPro S-Box': re.compile(r'^[0-9a-fA-F]{64}$'),
        'Whirlpool-0': re.compile(r'^[0-9a-fA-F]{128}$'),
        'Snefru-160': re.compile(r'^[0-9a-fA-F]{40}$'),
        'Haval-128,3': re.compile(r'^[0-9a-fA-F]{32}$'),
        'MD4': re.compile(r'^[0-9a-fA-F]{32}$'),
        # Add more hash formats here
    }

    # Determine hash type based on the provided hash
    hash_type = None
    for type_, regex in hash_formats.items():
        if regex.match(hash_input):
            hash_type = type_
            break

    if hash_type is None:
        return 'Invalid hash format'

    # Introduce a delay between tasks to avoid rate limiting
    async def check_and_delay(password, delay=0.1):
        await asyncio.sleep(delay)
        return f'Password found: {password} for hash type: {hash_type}'

    with open(rockyou_path, 'r', encoding='latin-1') as file:
        for password in file:
            password = password.strip()

            hashed_password = hash_password(password, hash_type)
            if hashed_password == hash_input:
                return await check_and_delay(password)

    return f'No password match found for the given hash type'

def hash_password(password, hash_type):
    """
    Hashes a password using the specified hash type

    Example usage: hash_password('password123', 'MD5')
    """
    if hash_type == 'MD5':
        return hashlib.new('md5', password.encode()).hexdigest()
    elif hash_type == 'SHA-1':
        return hashlib.new('sha1', password.encode()).hexdigest()
    elif hash_type == 'SHA-256':
        return hashlib.new('sha256', password.encode()).hexdigest()
    elif hash_type == 'SHA-512':
        return hashlib.new('sha512', password.encode()).hexdigest()
    elif hash_type == 'bcrypt':
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    elif hash_type == 'NTLM':
        return hashlib.new('md4', password.encode('utf-16le')).hexdigest()
    elif hash_type == 'LM':
        return hashlib.new('lm', password.encode()).hexdigest()[:16]
    elif hash_type == 'RipeMD-160':
        return hashlib.new('ripemd160', password.encode()).hexdigest()
    elif hash_type == 'Whirlpool':
        return hashlib.new('whirlpool', password.encode()).hexdigest()
    elif hash_type == 'Tiger-160':
        return hashlib.new('tiger192,3', password.encode()).hexdigest()[:40]
    elif hash_type == 'GOST R 34.11-94':
        return hashlib.new('gost94', password.encode()).hexdigest()
    # Add more hash algorithms here if needed

    return None  # Return None if the hash_type is not recognized

# Command: Time
@bot.command(name='time')
async def get_time(ctx, timezone_str=None):
    """
    Displays the current time in the specified timezone or the user's set timezone.

    Example command: ^time UTC
    """
    if timezone_str:
        await display_time(ctx, timezone_str)
    else:
        user_timezone = get_user_timezone(ctx.author)
        await display_time(ctx, user_timezone.zone)

async def display_time(ctx, timezone_str):
    try:
        user_timezone = get_user_timezone(ctx.author) if timezone_str is None else get_timezone(timezone_str)
    except ValueError as e:
        return await ctx.send(str(e))

    current_time = datetime.now(timezone.utc).astimezone(user_timezone)
    await ctx.send(f'The current time is: {current_time.strftime("%Y-%m-%d %H:%M:%S %Z")}')

def get_timezone(timezone_str):
    """
    Retrieves the timezone object based on the provided timezone string.

    Example usage: get_timezone('America/New_York')
    """
    try:
        # Attempt to create timezone using standard format
        return pytz.timezone(timezone_str)
    except pytz.UnknownTimeZoneError:
        pass

    # Try to map common abbreviations to timezone names
    abbreviations_mapping = {
        'PST': 'America/Los_Angeles',
        'JST': 'Asia/Tokyo',
        'EST': 'America/New_York',
        'CST': 'America/Chicago',
        'MST': 'America/Denver',
        'PDT': 'America/Los_Angeles',
        'MDT': 'America/Denver',
        'CDT': 'America/Chicago',
        'EDT': 'America/New_York',
        # ... (other abbreviations)
    }

    # UTC offsets mapping
    utc_offsets_mapping = {
        'UTC+00:00': 'UTC',
        'UTC+01:00': 'Europe/London',
        'UTC+02:00': 'Europe/Paris',
        'UTC+03:00': 'Europe/Moscow',
        'UTC+04:00': 'Asia/Dubai',
        'UTC+05:00': 'Asia/Karachi',
        'UTC+06:00': 'Asia/Dhaka',
        'UTC+07:00': 'Asia/Bangkok',
        'UTC+08:00': 'Asia/Shanghai',
        'UTC+09:00': 'Asia/Tokyo',
        'UTC+10:00': 'Australia/Sydney',
        'UTC+11:00': 'Pacific/Noumea',
        'UTC+12:00': 'Pacific/Fiji',
        'UTC-01:00': 'Atlantic/Azores',
        'UTC-02:00': 'America/Noronha',
        'UTC-03:00': 'America/Argentina/Buenos_Aires',
        'UTC-04:00': 'America/New_York',
        'UTC-05:00': 'America/Chicago',
        'UTC-06:00': 'America/Denver',
        'UTC-07:00': 'America/Los_Angeles',
        'UTC-08:00': 'America/Anchorage',
        'UTC-09:00': 'Pacific/Gambier',
        'UTC-10:00': 'Pacific/Honolulu',
        'UTC-11:00': 'Pacific/Pago_Pago',
        'UTC-12:00': 'Pacific/Wake',
    }

    mapped_timezone = abbreviations_mapping.get(timezone_str) or utc_offsets_mapping.get(timezone_str)
    if mapped_timezone:
        return pytz.timezone(mapped_timezone)

    raise ValueError(f'Invalid timezone "{timezone_str}". Please provide a valid timezone like "America/New_York", "UTC+05:00", "PST", "JST", etc.')

def get_user_timezone(user):
    """
    Retrieves the user's timezone based on their Discord user ID from the JSON file.
    Assumes the user ID is the key in the JSON file.

    Example usage: get_user_timezone(ctx.author)
    """
    try:
        with open(timezones_file, 'r') as file:
            user_timezones = json.load(file)
            timezone_str = user_timezones.get(str(user.id), 'UTC')
            return get_timezone(timezone_str)
    except FileNotFoundError:
        return get_timezone('UTC')  # Return UTC timezone by default

# Command: Help
@bot.command(name='help')
async def custom_help(ctx):
    help_intro = (
   "### General Commands \n"
        "- `^help`: A general help command that lists out all of the commands the bot supports and provides general usage information as well as command examples\n"
        "- `^advanced_help`: Shows the help page for advanced commands.\n"
        "- `^whoami`: Provides information about the bot, including its purpose and how to contribute.\n"
        "- `^hello`: A greeting/testing command. This command should just respond with 'Hello!' and is mainly just used as a sort of ping command to make sure the bot is up\n"
        "- `^dog`: Gives you a random picture of a dog \n"
        "- `^time`: Displays the time and allows for an optional timezone argument that supports a variety of timezone formats (ETC, UTC+04:00, America/New_York). If no timezone argument is given by the user than it will default to the user's set timezone, if the user has no set timezone than it will default to UTC time.\n"
        "  - Examples:\n"
        "    - `^time JST`\n"
        "    - `^time UTC-06:00`\n"
        "    - `^time Asia/Shanghai`\n"
        "- `^settimezone [timezone]`: Sets the timezone for the user running the command (this will be their default timezone when running the `^time` command with no provided timezone argument). Supports all of the known timezone formats that the `^time` command does.\n"
        "  - Example: `^settimezone America/Anchorage`\n"
   "### Technical Commands \n"
        "- `^crack [hash]`: Identifies the hash type provided and then attempts to crack the hash with the rockyou.tct wordlist. If the hash it cracked it will output the password and the hash type. If the password is not found the user will be informed that that is the case.\n"
        "  - Example: `^crack 68e109f0f40ca72a15e05cc22786f8e6`\n"
        "- `^URL_Checker [URL]`: Runs the provided URL against the Google's Safe Browsing database to try and determine is the URL is safe or not and then outputs that information to the user.\n"
        "  - Example: `^URL_Checker https://google.com`\n"
    )

    await ctx.send(help_intro)

@bot.command(name='advanced_help')
async def advanced_help(ctx):
    """
    Displays help information for advanced commands.
    """
    help_text = (
        "### Advanced Commands \n"
        "> Note: the bot does not store any of the emails/passwords you run through these commands, even in the logs, but if still do not want to risk exposing this information you can do to the Have I Been Pwned website or self host the bot to achieve the same results with less risk on your part. These commands are mostly a proof of concept and are not the best way at making sure your data is secure. \n"
        "- `^advanced_commands`: A command used to enable or disable all of the advanced commands of this discord bot, it is set to disabled by default.\n"
        "  - Examples:\n"
        "    - `^advanced_commands enable`\n"
        "    - `^advanced_commands disable`\n"
        "- `^email_checker`: This command will take the provided email and check it against Have I Been Pwned database to see if it has been exposed in any known breaches. Please do **NOT** provide your email as an argument for the command, the bot will DM you for the email after you run the `^email_checker` command with no arguments. \n"
        "- `^password_checker`: This command will take the provided password and check it against Have I Been Pwned database to see if it has been exposed in any known breaches. Please do **NOT** provide your password as an argument for the command, the bot will DM you for the email after you run the `^password_checker` command with no arguments.\n"
    )

    await ctx.send(help_text)

# Command: Settimezone
@bot.command(name='settimezone')
async def set_user_timezone(ctx, timezone_str):
    """
    Sets the timezone for the user in the server.

    Example command: ^settimezone UTC
    """
    try:
        user_timezone = get_timezone(timezone_str)
    except ValueError as e:
        return await ctx.send(str(e))

    save_user_timezone(ctx.author.id, timezone_str)
    await ctx.send(f'Timezone set to {timezone_str} for {ctx.author.display_name}')

def save_user_timezone(user_id, timezone_str):
    """
    Saves the user's timezone to a JSON file.

    Example usage: save_user_timezone(ctx.author.id, 'UTC')
    """
    try:
        with open(timezones_file, 'r') as file:
            user_timezones = json.load(file)
    except FileNotFoundError:
        user_timezones = {}

    user_timezones[str(user_id)] = timezone_str

    with open(timezones_file, 'w') as file:
        json.dump(user_timezones, file)

# Command: URL_Checker
@bot.command(name='URL_Checker')
async def check_url_safety(ctx, url):
    """
    Checks the safety of a given URL using Google Safe Browsing API.

    :param url: The URL to check.
    """
    async with ctx.typing():
        result = await check_url_safety_google_api(url)
    await ctx.send(result)

async def check_url_safety_google_api(url):
    """
    Checks the safety of a given URL using Google Safe Browsing API.

    :param url: The URL to check.
    :return: A message indicating whether the URL is safe or not.
    """

    # Google Safe Browsing API Endpoint
    api_endpoint = 'https://safebrowsing.googleapis.com/v4/threatMatches:find'

    # Request payload
    payload = {
        "client": {
            "clientId": "your-client-id",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "THREAT_TYPE_UNSPECIFIED", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }

    # Headers
    headers = {
        "Content-Type": "application/json"
    }

    # Send request to Google Safe Browsing API
    response = requests.post(f"{api_endpoint}?key={google_api_key}", json=payload, headers=headers)

    # Check response
    if response.status_code == 200:
        json_response = response.json()
        if 'matches' in json_response and json_response['matches']:
            return f"The URL '{url}' is NOT safe according to Google Safe Browsing API."
        else:
            return f"The URL '{url}' is safe according to Google Safe Browsing API."
    else:
        return f"Failed to check the safety of the URL '{url}' using Google Safe Browsing API."

# Command whoami
@bot.command(name='whoami')
async def who_am_i(ctx):
    whoami_message = (
        "I am a Discord bot built in Python and made by HiroNewf. I provide many different commands, "
        "but my main focus is useful cybersecurity commands for both technical and non-technical users alike. "
        "I am very much a work in progress and will continue to get new commands and updates as time goes on. "
        "For now, my primary functions are telling the time in any timezone, cracking password hashes with the "
        "rockyou.txt wordlist, and checking URLs for suspicious content using the Google Safe Browsing API. "
        "Feel free to contribute to me or fork and/or self-host me and use me for your own purposes. "
        "I am and will continue to be a completely open-source project. To see my code go to my GitHub page [here]"
        "(https://github.com/HiroNewf/PWN_Discord_Bot)."
    )

    await ctx.send(whoami_message)

@bot.command(name='advanced_commands')
@commands.has_permissions(administrator=True)
async def advanced_commands(ctx, action):
    """
    Enable or disable advanced commands.

    Example command to enable: ^advanced_commands enable
    Example command to disable: ^advanced_commands disable
    """
    global advanced_commands_enabled

    if action.lower() == 'enable':
        advanced_commands_enabled = True
        await ctx.send("Advanced commands are now enabled.")
    elif action.lower() == 'disable':
        advanced_commands_enabled = False
        await ctx.send("Advanced commands are now disabled.")
    else:
        await ctx.send("Invalid action. Please use 'enable' or 'disable'.")
        
# Command: email_checker
@bot.command(name='email_checker')
async def email_checker(ctx, email=None):
    """
    Checks if the provided email has been exposed in data breaches using Have I Been Pwned.
    Sends the email check result as a private message to the user.

    Example command: ^email_checker
    """
    global advanced_commands_enabled

    if not advanced_commands_enabled:
        await ctx.send("Advanced commands are currently disabled. Please ask a server admin to enable them using the `^advanced_commands enable` command")
        return

    if ctx.message.guild and email:
        # If used in a public channel with an argument, warn the user
        warning_message = await ctx.send("Please do not expose emails publicly. Use this command without an email and the bot will DM you for the required email.")
        await warning_message.delete(delay=10)  # Delete the warning message after 10 seconds

        # Delete the user's message
        await ctx.message.delete()
        return

    if email is None:
        # Send a direct message to the user to request their email
        await ctx.author.send("Please enter the email you want to check (visible only to you and the bot):")

        def check_author(message):
            return message.author == ctx.author and message.channel.type == discord.ChannelType.private

        try:
            # Wait for the user's response in a private message
            response_message = await bot.wait_for('message', check=check_author, timeout=60)
            email = response_message.content.strip()

        except TimeoutError:
            await ctx.author.send("Email check timed out. Please try the command again.")
            return

    # Perform email breach check
    result = await check_email_breach(email)

    # Send the result as a private message
    await ctx.author.send(result)

async def check_email_breach(email):
    """
    Performs an email breach check using the Have I Been Pwned service.

    :param email: The email to check.
    :return: A message indicating if the email has been exposed in data breaches.
    """
    # Send the email to the Have I Been Pwned service
    hibp_api_url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}'
    headers = {'User-Agent': 'PWN/1.0', 'hibp-api-key': hibp_api_key}

    response = requests.get(hibp_api_url, headers=headers)

    if response.status_code == 200:
        return f"The email '{email}' has been exposed in data breaches. It is recommended to update your credentials."
    elif response.status_code == 404:
        return f"The email '{email}' has not been exposed in known data breaches. It is considered safe."
    else:
        return f"Failed to check email breaches. Status code: {response.status_code}"

# Command: password_checker
@bot.command(name='password_checker')
async def password_checker(ctx, password=None):
    """
    Checks if the provided password has been exposed in data breaches using Have I Been Pwned.
    Sends the password check result as a private message to the user.

    Example command: ^password_checker
    """
    global advanced_commands_enabled

    if not advanced_commands_enabled:
        await ctx.send("Advanced commands are currently disabled. Please ask a server admin to enable them using the `^advanced_commands enable` command")
        return

    if ctx.message.guild and password:
        # If used in a public channel with an argument, warn the user
        warning_message = await ctx.send("Please do not expose passwords publicly. Use this command without a password and the bot will DM you for the required password.")
        await warning_message.delete(delay=10)  # Delete the warning message after 10 seconds

        # Delete the user's message
        await ctx.message.delete()
        return

    if password is None:
        # Send a direct message to the user to request their password
        await ctx.author.send("Please enter the password you want to check (visible only to you and the bot):")

        def check_author(message):
            return message.author == ctx.author and message.channel.type == discord.ChannelType.private

        try:
            # Wait for the user's response in a private message
            response_message = await bot.wait_for('message', check=check_author, timeout=60)
            password = response_message.content.strip()

        except TimeoutError:
            await ctx.author.send("Password check timed out. Please try the command again.")
            return

    # Perform password breach check
    result = await check_password_breach(password)

    # Send the result as a private message
    await ctx.author.send(result)

async def check_password_breach(password):
    """
    Performs a password breach check using the Pwned Passwords service.

    :param password: The password to check.
    :return: A message indicating if the password has been exposed in data breaches.
    """
    # Calculate the SHA-1 hash of the password
    sha1_password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    # Send the first 5 characters of the hash to the Pwned Passwords service
    prefix, suffix = sha1_password_hash[:5], sha1_password_hash[5:]
    pwned_api_url = f'https://api.pwnedpasswords.com/range/{prefix}'
    
    response = requests.get(pwned_api_url)

    if response.status_code == 200:
        # Check if the suffix (remainder of the hash) is present in the response
        breaches = [line.split(':') for line in response.text.splitlines()]
        matching_suffix = next((suffix for suffix, count in breaches if suffix == suffix), None)

        if matching_suffix:
            return f"The password has been exposed times in data breaches. It is not secure to use."
        else:
            return "The password has not been exposed in known data breaches. It is considered safe to use."

    else:
        return f"Failed to check password breaches. Status code: {response.status_code}"

# Command dog
@bot.command(name='dog')
async def dog(ctx):
    """
    Sends a random dog picture from the 'Dog' folder as an embedded image.
    
    Example command: ^dog
    """
    dog_folder = 'Dog'

    # Get a list of all files in the 'Dog' folder
    dog_files = [f for f in os.listdir(dog_folder) if os.path.isfile(os.path.join(dog_folder, f))]

    if not dog_files:
        await ctx.send("No dog pictures found.")
        return

    # Select a random dog picture
    random_dog = random.choice(dog_files)

    # Create an embedded message with the dog picture
    embed = discord.Embed(title="Here is your random dog picture", color=discord.Color.blue())
    embed.set_image(url=f"attachment://{random_dog}")

    # Send the embedded message with the dog picture
    await ctx.send(embed=embed, file=discord.File(os.path.join(dog_folder, random_dog), random_dog))
    
# Bot Token
bot.run(bot_token)
