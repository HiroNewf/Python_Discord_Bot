import discord
from discord.ext import commands
import asyncio

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello')
    async def say_hello(self, ctx):
        await ctx.send('Hello!')

async def setup(bot):
    await bot.add_cog(Hello(bot))

