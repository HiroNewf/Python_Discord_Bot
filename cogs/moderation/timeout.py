import discord
from discord.ext import commands

class Timeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="timeout")
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, time: int, *, reason=None):
        try:
            duration = discord.utils.utcnow() + discord.timedelta(seconds=time)
            await member.timeout_until(duration, reason=reason)
            await ctx.send(f"{member.mention} has been timed out for {time} seconds.")
        except discord.Forbidden:
            await ctx.send("I do not have permission to timeout this member.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(Timeout(bot))
