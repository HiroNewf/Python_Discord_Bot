from discord.ext import commands

class ForFoxSake(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='forfoxsake')
    async def forfoxsake(self, ctx):
        await ctx.send("https://forfoxsake.dev/")

async def setup(bot):
    await bot.add_cog(ForFoxSake(bot))
