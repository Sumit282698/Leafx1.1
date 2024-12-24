import discord, os
import datetime
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def hi(self, ctx):
        await ctx.send("hello user")


    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(title='Ping',description=f"```◪ Leaf Ping: {round(self.bot.latency * 1000)} ms\n ◪ Latency: 24\n```", color=discord.Color.green())
        embed.set_footer(text=f"{ctx.author.display_name}",icon_url=ctx.author.avatar)
        embed.timestamp= datetime.datetime.utcnow()
        await ctx.send(embed=embed)
        
    @commands.command()
    async def say(self, ctx, message=None):
        await ctx.send(message)


async def setup(bot):
    await bot.add_cog(Commands(bot))