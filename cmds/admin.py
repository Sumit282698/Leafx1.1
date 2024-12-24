import discord, os
import datetime
from discord.ext import commands
#class
class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
#admin command are here
#kick
    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def kick(self, ctx, member: discord.Member, reason='No Reason'):
        if member == None:
            embed=discord.Embed(title="Kick ", color=discord.Color.red(), description=f"{ctx.message.author} please enter a valid username!")

        else:
            guild = ctx.guild
            embed = discord.Embed(title="Kicked!", description=f"{member.mention} has been kicked!!", colour=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Reason: ", value=reason, inline=False)
            await ctx.reply(embed=embed)
            await guild.kick(user=member)

#purge
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def purge(self, ctx, amount=6):
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(title=f"{amount} messages has been purged!", colour=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed)

#mute
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        embed = discord.Embed(title="Muted", description=f"{member.mention} was muted ", colour=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.reply(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(f"You have been muted from: {guild.name} Reason: {reason}")

#unmute
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        await member.send(f"You have unmuted from: {ctx.guild.name}")
        embed = discord.Embed(title="Unmute", description=f"Unmuted {member.mention}", colour=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(admin(bot))