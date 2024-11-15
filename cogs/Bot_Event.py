import discord
import asyncio
from discord.ext import commands

from module.channleList import List

class Bot_Event(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot     

    #被伺服器移除時刪除所有註冊頻道
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        for channel in guild.text_channels:
            if channel.id in List.List:
                await List.delete(channel.id)
                
async def setup(bot: commands.Bot):
    await bot.add_cog(Bot_Event(bot))