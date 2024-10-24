from discord.ext import commands

class FivePillars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='fivepillars')
    async def five_pillars(self, ctx):
        await ctx.send("https://github.com/DFIRmadness/5pillars/blob/master/5-Pillars.md")

async def setup(bot):
    await bot.add_cog(FivePillars(bot))
