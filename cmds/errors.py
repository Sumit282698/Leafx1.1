import discord, os
import datetime
from discord.ext import commands
#class
class errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            if isinstance(error, commands.MissingPermissions):
                
                await ctx.reply(f"{error.missing_permissions} {error.args}")
            else:
                await ctx.send(f"{error}")
                print(f"{error}")
        except Exception as error:
            print(f"{error}")



async def setup(bot):
    await bot.add_cog(errors(bot))