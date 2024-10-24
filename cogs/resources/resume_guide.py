from discord.ext import commands

class ResumeGuide(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='resumeguide')
    async def resume_guide(self, ctx):
        await ctx.send("https://hironewf.vercel.app/Resume-Guide")

async def setup(bot):
    await bot.add_cog(ResumeGuide(bot))
