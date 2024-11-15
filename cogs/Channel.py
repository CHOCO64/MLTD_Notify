import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from typing import Optional

from module.channleList import List

class Channel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot     

    @app_commands.command(description = "註冊要接收提醒的頻道,未輸入名稱則註冊使用指令的該頻道")
    @app_commands.describe(channel = "請輸入頻道名稱")
    async def channel_notify(self, interaction: discord.Interaction, channel:Optional[discord.TextChannel] = None):
        if channel == None:
            register_channel = interaction.channel_id
        else:
            register_channel = channel.id

        channel_url = "https://discord.com/channels/"+str(interaction.guild_id)+"/"+str(register_channel)
        if await List.add(register_channel):
            await interaction.response.send_message(f"{channel_url} 註冊成功")
        else:
            await interaction.response.send_message(f"{channel_url} 已經註冊過了")

        
    @app_commands.command(description = "移除要接收提醒的頻道,未輸入名稱則移除使用指令的該頻道")
    @app_commands.describe(channel = "請輸入頻道名稱")
    async def remove_channel_notify(self, interaction: discord.Interaction, channel:Optional[discord.TextChannel] = None):
        if channel == None:
            register_channel = interaction.channel_id
        else:
            register_channel = channel.id

        channel_url = "https://discord.com/channels/"+str(interaction.guild_id)+"/"+str(register_channel)
        
        if await List.delete(register_channel):
            await interaction.response.send_message(f"{channel_url} 已移除")
        else:
            await interaction.response.send_message(f"{channel_url} 未註冊")
                
async def setup(bot: commands.Bot):
    await bot.add_cog(Channel(bot))