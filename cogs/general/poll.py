import discord
from discord.ext import commands
import asyncio

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='poll')
    async def poll(self, ctx, question, *options):
        if len(options) < 2:
            await ctx.send("You need to provide at least two options for the poll.")
            return

        if len(options) > 9:
            await ctx.send("You can only provide up to 9 options.")
            return

        description = "\n".join([f"{emoji} {option}" for emoji, option in zip("🇦🇧🇨🇩🇪🇫🇬🇭🇮", options)])
        embed = discord.Embed(title=question, description=description, color=discord.Color.blue())

        message = await ctx.send(embed=embed)
        for emoji in "🇦🇧🇨🇩🇪🇫🇬🇭🇮"[:len(options)]:
            await message.add_reaction(emoji)

async def setup(bot):
    await bot.add_cog(Poll(bot))
