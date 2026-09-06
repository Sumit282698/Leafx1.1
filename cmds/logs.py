import discord, os, json, datetime
from discord.ext import commands

CONFIG_FILE = 'data/serverslogs.json'

def load_file():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_file(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)


#class
class logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # setup Cmds
    @commands.command(name="logall")
    @commands.has_permissions(moderate_members=True)
    async def set_logger(self, ctx, channel: discord.TextChannel):
        """
        Used To log all messages in a single channel.
        Usage: !logall <#channel>
        """
        config = load_file()
        server_id = str(ctx.author.guild.id)
        if server_id not in config:
            config[server_id] = {}
        config[server_id]['message_logs'] = channel.id
        config[server_id]['join_logs'] = channel.id
        config[server_id]['members_logs'] = channel.id
        config[server_id]['mod_logs'] = channel.id
        config[server_id]['automod_logs'] = channel.id

        save_file(config)

        embed = discord.Embed(title="Leaf's Logger", description=f"> **All Log Channel set to** {channel.mention} **Now all the Logs Will be sent to this channel.**", color=discord.Colour.brand_green())
        embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


    @commands.command(name="logmessages")
    @commands.has_permissions(moderate_members=True)
    async def message_logger(self, ctx, channel: discord.TextChannel):
        """
        Usage: !logmessages <#channel>
        """
        config = load_file()
        server_id = str(ctx.author.guild.id)

        if server_id not in config:
            config[server_id] = {}
        config[server_id]['message_logs'] = channel.id
        save_file(config)
        embed = discord.Embed(title="Leaf's Message Logger", description=f"> **Message Logger Channel set to** {channel.mention} **Now all the Edited and Deleted Messages Will go to this channel.**", color=discord.Colour.brand_green())
        embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="logroles")
    @commands.has_permissions(moderate_members=True)
    async def message_logger(self, ctx, channel: discord.TextChannel):
        """
        Usage: !logroles <#channel>
        """
        config = load_file()
        server_id = str(ctx.author.guild.id)

        if server_id not in config:
            config[server_id] = {}
        config[server_id]['role_logs'] = channel.id
        save_file(config)
        embed = discord.Embed(title="Leaf's Roles Logger", description=f"> **Role Logger Channel set to** {channel.mention} **Now all the Role Updates Will go to this channel**.", color=discord.Colour.brand_green())
        embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="logmembers")
    @commands.has_permissions(moderate_members=True)
    async def message_logger(self, ctx, channel: discord.TextChannel):
        """
        Usage: !logmembers <#channel>
        """
        config = load_file()
        server_id = str(ctx.author.guild.id)

        if server_id not in config:
            config[server_id] = {}
        config[server_id]['members_logs'] = channel.id
        save_file(config)
        embed = discord.Embed(title="Leaf's Message Logger", description=f"> **Member Logger Channel set to** {channel.mention} **Now all the Avatar Updates and Nick Names will go to this channel>**", color=discord.Colour.brand_green())
        embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)






#logs are here    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Message Edit Logs"""
        if before.guild is None:
            return
        if after.author.bot:
            return
        if before.content == after.content:
            return
        config = load_file()
        server_id = str(before.guild.id)

        if server_id in config and 'message_logs' in config[server_id]:
            log_channel_id = config[server_id]['message_logs']
            log_channel = before.guild.get_channel(log_channel_id)

        if log_channel:
            embed= discord.Embed(title="Message Update", colour=discord.Colour.yellow(),description=f"> **Author:** {before.author.mention} ({before.author.name})\n", timestamp=datetime.datetime.utcnow())
            embed.add_field(name="__Message Before__", value=f"{before.content}")
            embed.add_field(name="__Message After Editing__", value=f"{after.content}")
            embed.set_footer(text=(f"{after.author.display_name}"), icon_url=after.author.avatar)
            await log_channel.send(embed=embed)
                

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Message Delete Logs"""
        if message.author.bot:
            return

        config = load_file()
        server_id = str(message.guild.id)

        if server_id in config and 'message_logs' in config[server_id]:
            log_channel_id = config[server_id]['message_logs']
            log_channel = message.guild.get_channel(log_channel_id)

            if log_channel:
                embed = discord.Embed(title="Message Deleted", color=discord.Colour.red(), description=f"**Author:** {message.author.mention} ({message.author.name})\n**Channel:** {message.channel.mention}\n**Message ID:** `{message.id}`", timestamp=datetime.datetime.utcnow())
                embed.add_field(name="__Content:__", value=f"{message.content}")
                embed.set_footer(text=f"{message.author.display_name}", icon_url=message.author.avatar.url)
                embed.timestamp = discord.utils.utcnow()
                await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Member Update Logs"""
        config = load_file()
        server_id = str(before.guild.id)

        if server_id in config and 'members_logs' in config[server_id]:
            log_channel_id = config[server_id]['members_logs']
            log_channel = before.guild.get_channel(log_channel_id)

        if log_channel:
            if before.nick != after.nick:
                embed = discord.Embed(title="Nick Name Update", description=f"**Author:** {before.mention} ({before.name})", color=discord.Colour.blurple(), timestamp=datetime.datetime.utcnow())
                embed.add_field(name="Old Nick Name:",value=f"{before.nick}",  inline=False)
                embed.add_field(name="New Nick Name:",value=f" {after.nick}", inline=False)
                embed.set_thumbnail(url=after.avatar.url)
                await log_channel.send(embed=embed)

            if before.roles != after.roles:
                added_roles = [role for role in after.roles if role not in before.roles and role.id != after.guild.id]
                removed_roles = [role for role in before.roles if role not in after.roles and role.id != before.guild.id]
                
                embed = discord.Embed(title="Role Update", description=f"**Author:** {before.mention} ({before.name})", color=discord.Colour.blurple(), timestamp=datetime.datetime.utcnow())
                embed.set_thumbnail(url=before.avatar.url)

                if added_roles:
                    role_names = ", ".join([role.mention for role in added_roles])
                    embed.add_field(name="<a:tick:1388870030057410691> __Roles Added__", value="".join(role_names))
                    await log_channel.send(embed=embed)
                if removed_roles:
                    role_names = ", ".join([role.mention for role in removed_roles])
                    embed.add_field(name="<a:cross:1388869982619697152> __Roles Removed__", value="".join(role_names))
                    await log_channel.send(embed=embed)
        else:
            return
            
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        config = load_file()
        server_id = str(member.guild.id)

        if server_id in config and 'join_logs' in config[server_id]:
            log_channel_id = config[server_id]['join_logs']
            log_channel = member.guild.get_channel(log_channel_id)
            embed = discord.Embed(title="Member Joined", description=f"**Member:** {member.mention} (`{member.name}`)", colour=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=member.display_avatar.url)
            await log_channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        config = load_file()
        server_id = str(member.guild.id)

        if server_id in config and 'join_logs' in config[server_id]:
            log_channel_id = config[server_id]['join_logs']
            log_channel = member.guild.get_channel(log_channel_id)
            embed = discord.Embed(title="Member Left", description=f"**Member:** {member.mention} (`{member.name}`)", colour=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=member.display_avatar.url)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        config = load_file()
        server_id = str(guild.id)

        if server_id in config and 'mod_logs' in config[server_id]:
            log_channel_id = config[server_id]['mod_logs']
            log_channel = guild.get_channel(log_channel_id)
        if log_channel:
            embed=discord.Embed(title="Member Banned", description=f"**Member:** {user.mention} (`{user.name}`)\nThis User Has been Banned From the Server" , color=discord.Colour.brand_red(), timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=user.display_avatar.url)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user):
        config = load_file()
        server_id = str(guild.id)

        if server_id in config and 'mod_logs' in config[server_id]:
            log_channel_id = config[server_id]['mod_logs']
            log_channel = guild.get_channel(log_channel_id)
        if log_channel:
            embed=discord.Embed(title="Member UnBanned", description=f"**Member:** {user.mention} (`{user.name}`)\nThis User Has been UnBanned From the Server" , color=discord.Colour.brand_red(), timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=user.display_avatar.url)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.Member, after: discord.Member):
        if before.bot:
            return
        config = load_file()
        server_id = str(before.guild.id)
        log_channel_id = None
        log_channel = None
        if 'member_logs' in config[server_id]:
            log_channel_id = config[server_id]['member_logs']
            try:
                log_channel = self.bot.get_channel(int(log_channel_id))
            except ValueError:
                print(f"Error: Invalid channel ID format '{log_channel_id}' for server {server_id}. Must be an integer.")
                return
        if log_channel_id:
            if after.avatar != before.avatar:
                embed=discord.Embed(title="Avatar Update", description=f"**User:** {before.mention} ({after.name})", color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
                embed.set_thumbnail(url=after.display_avatar.url)
                await log_channel.send(embed=embed)

# Auto Moderation
    @commands.Cog.listener()
    async def on_automod_rule_create(self, rule):
        pass
    
    @commands.Cog.listener()
    async def on_automod_rule_update(self, rule):
        pass

    @commands.Cog.listener()
    async def on_automod_rule_delete(self, rule):
        pass


async def setup(bot):
    await bot.add_cog(logs(bot))