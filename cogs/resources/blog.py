from discord.ext import commands

class Blog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='blog')
    async def blog(self, ctx):
        await ctx.send("https://hironewf.vercel.app/")

async def setup(bot):
    await bot.add_cog(Blog(bot))
