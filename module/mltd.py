import asyncio
import aiohttp
import json
import os
from datetime import datetime,timezone,timedelta

class MLTD:
    def __init__(self):
        self.MLTD_Data = {
        "id" : 0,
        "type" : None,
        "name" : None,
        "beginAt" : None,
        "endAt" : None,
        "boostBeginAt" : None,
        "pageClosedAt" : None
        }
    
    # Get MLTD event data from ./data/mltd.json   
    async def load(self):
        if os.path.isfile("./data/mltd.json"):
            with open("./data/mltd.json", "r", encoding='utf-8') as mltdFile:
                Data = json.load(mltdFile)
                print("[Get_MLTD_data()]Get data Finish")
                self.MLTD_Data = Data
        else:
            print("[Get_MLTD_data()]mltd.json not exist,and call Updaet_MLTD_data()")
            await self.Get_data_from_API()
    
    # Get MLTD event data via matsurihi API       
    async def Get_data_from_API(self):
        trycount = 0
        while trycount < 5:
            try:
                async with aiohttp.request('GET', 'https://api.matsurihi.me/api/mltd/v2/events') as resp:
                    if resp.status == 200 :
                        posts = await resp.json()
                        print("[Get_MLTD_data_from_API()]Get MLTD data success")
                        for data in posts[-1:]:
                            if self.MLTD_Data['id'] < data['id']:
                                self.MLTD_Data = {
                                "id" : data['id'],
                                "type" : data['type'],
                                "name" : data['name'],
                                "beginAt" : data['schedule']['beginAt'],
                                "endAt" : data['schedule']['endAt'],
                                "boostBeginAt" : data['schedule']['boostBeginAt'],
                                "pageClosedAt" : data['schedule']['pageClosedAt']
                                }
                                await self.Update()
                                return True
                            else:
                                return False
            except Exception as e:  
                trycount += 1
                await asyncio.sleep(1)
                print(e)
                print("[Get_MLTD_data_from_API()]Get MLTD data retry", trycount, "times")
        if trycount == 5:
            return False
    
    #Update MLTD event data to ./data/mltd.json 
    async def Update(self):
        with open("./data/mltd.json", "w", encoding='utf-8') as NewFile:
            json.dump(self.MLTD_Data, NewFile, indent=4)
        print("[Updaet_MLTD_data()]Update data Finish")
        
    #type 3,4,5,11,13,16 => target event    
    def event_check(self):
        if self.MLTD_Data['type'] in [3,4,5,11,13,16]:
            return True
        else:
            return False
    
mltd = MLTD()   
    
    