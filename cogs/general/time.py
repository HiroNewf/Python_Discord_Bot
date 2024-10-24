import discord
from discord.ext import commands
from datetime import datetime, timezone
import pytz
import json
import asyncio

timezones_file = 'timezones.json'  # Adjust the path as needed

class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='time')
    async def get_time(self, ctx, timezone_str=None):
        """Displays the current time in the specified timezone or the user's set timezone."""
        if timezone_str:
            await self.display_time(ctx, timezone_str)
        else:
            user_timezone = self.get_user_timezone(ctx.author)
            await self.display_time(ctx, user_timezone.zone)

    @commands.command(name='settimezone')
    async def set_timezone(self, ctx, timezone_str):
        """Sets the user's timezone in the timezones file."""
        try:
            # Verify the provided timezone is valid
            user_timezone = self.get_timezone(timezone_str)
        except ValueError as e:
            return await ctx.send(str(e))
        
        # Update the user's timezone in the JSON file
        self.set_user_timezone(ctx.author, timezone_str)
        await ctx.send(f"Your timezone has been set to {timezone_str}.")

    async def display_time(self, ctx, timezone_str):
        try:
            user_timezone = self.get_timezone(timezone_str)
        except ValueError as e:
            return await ctx.send(str(e))

        current_time = datetime.now(timezone.utc).astimezone(user_timezone)
        await ctx.send(f'The current time is: {current_time.strftime("%Y-%m-%d %H:%M:%S %Z")}')

    def get_timezone(self, timezone_str):
        """
        Retrieves the timezone object based on the provided timezone string.
        """
        try:
            return pytz.timezone(timezone_str)
        except pytz.UnknownTimeZoneError:
            pass

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
        }

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

    def get_user_timezone(self, user):
        """
        Retrieves the user's timezone based on their Discord user ID from the JSON file.
        """
        try:
            with open(timezones_file, 'r') as file:
                user_timezones = json.load(file)
                timezone_str = user_timezones.get(str(user.id), 'UTC')  # Default to UTC if not set
                return self.get_timezone(timezone_str)
        except FileNotFoundError:
            return self.get_timezone('UTC')  # Return UTC timezone by default

    def set_user_timezone(self, user, timezone_str):
        """
        Sets the user's timezone in the JSON file.
        """
        try:
            with open(timezones_file, 'r') as file:
                user_timezones = json.load(file)
        except FileNotFoundError:
            user_timezones = {}

        user_timezones[str(user.id)] = timezone_str

        with open(timezones_file, 'w') as file:
            json.dump(user_timezones, file, indent=4)

async def setup(bot):
    await bot.add_cog(Time(bot))
