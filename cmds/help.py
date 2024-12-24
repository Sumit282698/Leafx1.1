import discord, os
from discord.ext import commands
#class
class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
#help command are here
    @commands.command(name="help")
    async def help(self, ctx):
        desc="working"
        embed=discord.Embed(title="Help Menu", description="working ", color=discord.Color.green())
        embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)




async def setup(bot):
    await bot.add_cog(help(bot))