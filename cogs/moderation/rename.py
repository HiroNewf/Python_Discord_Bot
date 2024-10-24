import discord
from discord.ext import commands

class Rename(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rename")
    @commands.has_permissions(manage_nicknames=True)
    async def rename(self, ctx, member: discord.Member, *, new_nickname):
        try:
            old_nickname = member.nick if member.nick else member.name
            await member.edit(nick=new_nickname)
            await ctx.send(f"{old_nickname} has been renamed to {new_nickname}.")
        except discord.Forbidden:
            await ctx.send("I do not have permission to rename this member.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(Rename(bot))
