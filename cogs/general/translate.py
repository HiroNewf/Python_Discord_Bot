from googletrans import Translator
import discord
from discord.ext import commands
import asyncio

class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()

    @commands.command(name='translate')
    async def translate(self, ctx, language, *, text):
        try:
            translated = self.translator.translate(text, dest=language)
            await ctx.send(f"**Original:** {text}\n**Translated:** {translated.text}")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(Translate(bot))
