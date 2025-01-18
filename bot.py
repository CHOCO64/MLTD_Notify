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

#斜線指令有更新時記得用一下這個command
@bot.command()
@commands.is_owner()
async def sync(ctx):
    print("[Start sync]")
    await ctx.send(f"sync command start")
    slash = await bot.tree.sync()
    await ctx.send(f"載入 {len(slash)} 個斜線指令")
    await ctx.send(f"sync command end")
    print(f"載入 {len(slash)} 個斜線指令")

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    print("[Start load]")
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    print("[Start unload]")
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    print("[Start reload]")
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Reloaded {extension} done.")

async def load_extensions():
    print("[Start load_extensions]")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        print("[Start main]")
        await load_extensions()
        print("load config.json")
        with open("./config.json",mode="r",encoding="utf8") as f:
            data = json.load(f)
            if "botToken" not in data:
                raise ValueError("The 'botToken' field is required.")
            bot_token = data["botToken"]
        await bot.start(bot_token)

if __name__ == "__main__":
    asyncio.run(main())
