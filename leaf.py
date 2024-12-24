import discord
from discord.ext import commands
import os
import config
import asyncio

intents = discord.Intents.all()
bot= commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")
@bot.event
async def on_ready():
    activity = discord.Game(name="Leaf X PYTHON", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print(f'I am Online')
    await bot.tree.sync()

async def Load():
    for filename in os.listdir("./cmds"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cmds.{filename[:-3]}")
            print(f'Loaded Files {filename[:-3]}')

async def main():
    async with bot:
        await Load()
        await bot.start(config.Token)
asyncio.run(main())