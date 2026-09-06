import discord, os, json, config, asyncio, random
from discord.ext import commands, tasks
config_file = "data/config.json"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
members = len(bot.users)
guilds = len(bot.guilds)
activities_list = [
    discord.Activity(type=discord.ActivityType.listening, name="!help", state= "Playing With Python"),
    discord.Activity(type=discord.ActivityType.watching, name=f"{members} Members & {guilds} Guilds")
   ]
@tasks.loop(seconds=5)
async def change_activity():
    activity = random.choice(activities_list)
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.event
async def on_ready():
    print(f'Logged in as Leaf!')
    try:
        for filename in os.listdir("./cmds"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cmds.{filename[:-3]}")
                print(f"Loaded cog: {filename[:-3]}")
        print("x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x--x-x-x-x-x")
        print("Loaded all cogs successfully.")
    except Exception as e:
        print(f"{e}")
    await bot.tree.sync()
    change_activity.start()

if __name__ == "__main__":
    bot.run(config.Token)