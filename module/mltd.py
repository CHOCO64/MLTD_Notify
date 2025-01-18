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
    
    # 從 matsurihi API 取得目前最新的MLTD活動資料        
    async def Get_data_from_API(self):
        print("[Start MLTD.Get_MLTD_data_from_API()]")
        trycount = 0
        #最多retry五次
        while trycount < 5:
            try:
                async with aiohttp.request('GET', 'https://api.matsurihi.me/api/mltd/v2/events') as resp:
                    if resp.status == 200 :
                        posts = await resp.json()
                        print("Get MLTD data via API success")
                        for data in posts[-1:]:
                            print("Get newer data")
                            #有更新個資料才會更新
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
                                print("return True")
                                return True
                            else:
                                print("return False")
                                return False
            except Exception as e:  
                trycount += 1
                await asyncio.sleep(1)
                print(e)
                print("Get MLTD data via API retry", trycount, "times")
        print("return False")
        return False
    
    #type 3,4,5,11,13,16 => target event    
    async def Event_check(self):
        print("[Start MLTD.Event_check()]")
        if self.MLTD_Data['type'] in [3,4,5,11,13,16]:
            print("return True")
            return True
        else:
            print("return False")
            return False
    
mltd = MLTD()   
    
    