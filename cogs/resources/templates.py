from discord.ext import commands

class Templates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='templates')
    async def resume_templates(self, ctx):
        await ctx.send("https://github.com/HiroNewf/Cybersec_resume_examples")

async def setup(bot):
    await bot.add_cog(Templates(bot))
