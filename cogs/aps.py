import os
import discord
import asyncio
from discord.ext import commands
from datetime import datetime,timezone,timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json
import time

from module.mltd import mltd
from module.channleList import List

#轉換成UTC8時區的時間
def TZ2UTC8(datetimeString):
    GoodTime = datetime.strptime(datetimeString, "%Y-%m-%dT%H:%M:%S%z")
    return GoodTime.astimezone(timezone(timedelta(hours=8)))

class Task(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bgTask = AsyncIOScheduler(timezone=timezone(timedelta(hours=8)))
        self.UpdateTaskID = None 

    async def cog_load(self):
        #MLTD event資料 初始化
        await mltd.Get_data_from_API()
            
        #讀取已註冊頻道
        await List.load()
        
        #設定第一個task
        await self.Set_task()
        
        #scheduler啟動
        self.bgTask.start()
    
    #reload/unload aps.py時取消所有提醒    
    async def cog_unload(self):
        self.bgTask.shutdown()
    
    #設定提醒和資料更新的job
    async def Set_task(self):
        print("[Set_task]",datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S"))
        #活動頁關閉兩分鐘後,每10分鐘check一次
        Update_time = TZ2UTC8(mltd.MLTD_Data["pageClosedAt"])
        Update_time = Update_time + timedelta(minutes=2)
        job = self.bgTask.add_job(self.Update_task,'interval', start_date=Update_time, minutes=10)
        self.UpdateTaskID = job.id
        
        #設定下一個活動提醒
        if await mltd.Event_check():
            goodTime =  TZ2UTC8(mltd.MLTD_Data["beginAt"])
            goodTime2 = TZ2UTC8(mltd.MLTD_Data["endAt"])
            #活動期間,每天九點發送提醒
            self.bgTask.add_job(self.Notify_task, 'cron',start_date=goodTime,end_date=goodTime2, hour='9')
            
    #MLTD資料更新任務        
    async def Update_task(self):
        await self.bot.wait_until_ready()
        print("[Update_task]",datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S"))
        if await mltd.Get_data_from_API():
            #活動資料更新後取消目前的Update task
            self.bgTask.remove_job(self.UpdateTaskID)
            #設定新任務
            await self.Set_task()
            
            #第一天的提醒
            if await mltd.Event_check():
                await self.Notify_task()    
                
    #活動提醒        
    async def Notify_task(self):
        print("[Notify_task]",datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S"))
        await self.bot.wait_until_ready()
        if mltd.MLTD_Data["boostBeginAt"] == None:
            #For debug用的test command
            EndDate = TZ2UTC8(mltd.MLTD_Data["endAt"])
            day_remain = (EndDate.date() - datetime.now().date()).days
            embed=discord.Embed(title="打活動了!!", color=0x81d8d0)
            embed.add_field(name=mltd.MLTD_Data['name'], value="活動還剩: "+str(day_remain)+"天\n最後一天: "+mltd.MLTD_Data["endAt"][:10], inline=False)
        else:
            BoostDate = TZ2UTC8(mltd.MLTD_Data["boostBeginAt"])
            
            EndDate = TZ2UTC8(mltd.MLTD_Data["endAt"])
            day_remain = (EndDate.date() - datetime.now().date()).days
            
            if BoostDate.date() == datetime.now().date():
                embed=discord.Embed(title="打活動了!! 下午Boost!!", color=0x81d8d0)
                embed.add_field(name=mltd.MLTD_Data['name'], value="活動還剩: "+str(day_remain)+"天\n最後一天: "+mltd.MLTD_Data["endAt"][:10], inline=False)
            elif day_remain == 0:
                embed=discord.Embed(title="今天是最後一天了!!", color=0x81d8d0)
                embed.add_field(name=mltd.MLTD_Data['name'], value="結束時間: "+EndDate.strftime("%H:%M:%S"), inline=False)
            elif BoostDate.date() < datetime.now().date():
                embed=discord.Embed(title="打活動了!! Boost Now!!", color=0x81d8d0)
                embed.add_field(name=mltd.MLTD_Data['name'], value="活動還剩: "+str(day_remain)+"天\n最後一天: "+mltd.MLTD_Data["endAt"][:10], inline=False)
            else :
                embed=discord.Embed(title="打活動了!!", color=0x81d8d0)
                embed.add_field(name=mltd.MLTD_Data['name'], value="活動還剩: "+str(day_remain)+"天\n最後一天: "+mltd.MLTD_Data["endAt"][:10], inline=False)
        
        await self.Broadcast(embed)
    
    #channel廣播    
    async def Broadcast(self, embed):
        count = 0
        ListLen = len(List.List)
        while count < ListLen:
            channel = self.bot.get_channel(List.List[count])
            try:
                await channel.send(embed=embed)
            except:
                #10秒後再傳送一次
                time.sleep(10)
                await channel.send(embed=embed)
            count += 1

#以下皆是debug用command, 只有機器人owner可以執行
    
    @commands.command()
    @commands.is_owner()
    async def test(self, ctx):
        print("Test command")
        await self.Notify_task()

    @commands.command()
    @commands.is_owner()
    async def display(self, ctx):
        await ctx.send(mltd.MLTD_Data)

    @commands.command()
    @commands.is_owner()
    async def stop(self, ctx):
        self.bgTask.shutdown()
        await ctx.send('任務已停止')
        
    @commands.command()
    @commands.is_owner()
    async def start(self, ctx):
        self.bgTask.start()
        await ctx.send('任務開始')
        
    @commands.command()
    @commands.is_owner()
    async def remove(self, ctx, jobID:str):
        self.bgTask.remove_job(jobID)
        await ctx.send("任務已移除")
        
    @commands.command()
    @commands.is_owner()
    async def listjob(self, ctx):
        jobList = self.bgTask.get_jobs()
        count = 0
        jobNum = len(jobList)
        if jobNum > 0 :
            await ctx.send("目前已註冊的提醒如下:")
        else:
            await ctx.send("目前無任何提醒")
        while count < jobNum :
            job = self.bgTask.get_job(jobList[count].id)
            count += 1
            await ctx.send(f"{count}. {job} ID:{job.id}")
        
#以上皆是debug用command, 只有機器人owner可以執行  
                
async def setup(bot: commands.Bot):
    await bot.add_cog(Task(bot))