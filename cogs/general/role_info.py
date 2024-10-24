import discord
from discord.ext import commands
import asyncio

class RoleInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='role_info')
    async def role_info(self, ctx, *, role_name):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send("Role not found.")
            return

        members = [member.mention for member in ctx.guild.members if role in member.roles]
        member_list = "\n".join(members) if members else "No members with this role."

        embed = discord.Embed(title=f"Role Info: {role.name}", color=role.color)
        embed.add_field(name="ID", value=role.id)
        embed.add_field(name="Color", value=str(role.color))
        embed.add_field(name="Created At", value=role.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="Members", value=member_list)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RoleInfo(bot))
