import random
from discord.ext import commands

class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8ball")
    async def eight_ball(self, ctx, *, question):
        responses = [
            "Yes", "No", "Maybe", "Ask again later", "Definitely not", 
            "Absolutely", "I don't think so", "Yes, but..."
        ]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

async def setup(bot):
    await bot.add_cog(EightBall(bot))
