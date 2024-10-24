import os
import random
import discord
from discord.ext import commands

class Dog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dog")
    async def dog(self, ctx):
        """
        Sends a random dog picture from the 'Dog' folder as an embedded image.
        """
        dog_folder = 'Dog'

        # Get a list of all files in the 'Dog' folder
        dog_files = [f for f in os.listdir(dog_folder) if os.path.isfile(os.path.join(dog_folder, f))]

        if not dog_files:
            await ctx.send("No dog pictures found.")
            return

        # Select a random dog picture
        random_dog = random.choice(dog_files)

        # Create an embedded message with the dog picture
        embed = discord.Embed(title="Here is your random dog picture", color=discord.Color.blue())
        embed.set_image(url=f"attachment://{random_dog}")

        # Send the embedded message with the dog picture
        await ctx.send(embed=embed, file=discord.File(os.path.join(dog_folder, random_dog), random_dog))

async def setup(bot):
    await bot.add_cog(Dog(bot))
