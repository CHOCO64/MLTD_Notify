# 導入Discord.py模組
import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import json

# intents是要求機器人的權限
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = "!", intents = intents)


@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")

@bot.command()
@commands.is_owner()
async def sync(ctx):
    await ctx.send(f"sync command start")
    await bot.tree.sync()
    await ctx.send(f"sync command end")

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Reloaded {extension} done.")

async def load_extensions():
    print(f"load_extensions")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    print(f"main")
    async with bot:
        await load_extensions()
        with open("./config.json",mode="r",encoding="utf8") as f:
            data = json.load(f)
            if "botToken" not in data:
                raise ValueError("The 'botToken' field is required.")
            bot_token = data["botToken"]
        await bot.start(bot_token)

if __name__ == "__main__":
    asyncio.run(main())
