import discord
from discord.ext import commands
import re
import asyncio
from datetime import datetime, timezone
import pytz
import hashlib
import bcrypt
import json

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="^", intents=intents, help_command=None)

rockyou_path = 'rockyou.txt'
timezones_file = 'user_timezones.json'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='hello')
async def hello(ctx):
    """Greeting / Testing Command"""
    await ctx.send('Hello!')

@bot.command(name='crack')
async def identify_hash(ctx, hash_input):
    """
    Identifies the hash type and attempts to crack the password with rockyou.txt

    param:hash_input = The input hash to be identified and cracked
    """
    async with ctx.typing():
        result = await crack_password(hash_input)
    await ctx.send(result)

async def crack_password(hash_input):
    """
    Attempts to crack the password for a given hash with rockyou.txt

    param:hash_input: The input hash to be cracked
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

    :param password: The password to be hashed
    :param hash_type: The hash algorithm to use
    :return: The hashed password
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

    :param timezone_str: The timezone string.
    :return: The timezone object.
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
        'UTC': 'UTC',
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
        # ... (other UTC offsets)
    }

    mapped_timezone = abbreviations_mapping.get(timezone_str) or utc_offsets_mapping.get(timezone_str)
    if mapped_timezone:
        return pytz.timezone(mapped_timezone)

    raise ValueError(f'Invalid timezone "{timezone_str}". Please provide a valid timezone like "America/New_York", "UTC+05:00", "PST", "JST", etc.')

def get_user_timezone(user):
    """
    Retrieves the user's timezone based on their Discord user ID from the JSON file.
    Assumes the user ID is the key in the JSON file.

    :param user: The Discord user.
    :return: The user's timezone.
    """
    try:
        with open(timezones_file, 'r') as file:
            user_timezones = json.load(file)
            timezone_str = user_timezones.get(str(user.id), 'UTC')
            return get_timezone(timezone_str)
    except FileNotFoundError:
        return get_timezone('UTC')  # Return UTC timezone by default

@bot.command(name='help')
async def custom_help(ctx):
    """Displays a custom help message with information about available commands."""
    help_message = (
        f"**General Commands:**\n"
        "* `^hello`: A greeting/testing command, the bot should respond with 'Hello!'.\n"
        "* `^time [timezone]`: Displays the current time in the specified timezone or the user's set timezone.\n"
        " * Example: `^time UTC` or `^time America/New_York`\n"
	"**Technical Commands:**\n"
	"* `^crack <hash>`: Identifies the hash type and attempts to crack the password with the rockyou.txt worldlist. For more information on the hash types support reference the Github Page.\n"
        " *  Example: `^crack 68e109f0f40ca72a15e05cc22786f8e6`\n"
    )
    await ctx.send(help_message)

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

    :param user_id: The user's ID.
    :param timezone_str: The timezone string.
    """
    try:
        with open(timezones_file, 'r') as file:
            user_timezones = json.load(file)
    except FileNotFoundError:
        user_timezones = {}

    user_timezones[str(user_id)] = timezone_str

    with open(timezones_file, 'w') as file:
        json.dump(user_timezones, file)

bot.run('TOKEN')
