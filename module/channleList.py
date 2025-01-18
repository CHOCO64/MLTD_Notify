import asyncio
import json
import os

class Channel:
    def __init__(self):
        self.List = []
    
    #load data from json    
    async def load(self):
        print("[Start Channel.load()]")
        if os.path.isfile("./data/channle.json"):
            with open("./data/channle.json",mode="r",encoding="utf8") as channleFile:
                self.List = json.load(channleFile)
        else:
            await self.Save()
 
    #Save channle data to json 
    async def Save(self):
        print("[Start Channel.Save()]")
        with open("./data/channle.json", "w", encoding="utf8") as channleFile:
            json.dump(self.List, channleFile)
 
    #新增channle,並save至json  
    async def add(self, channle:int):
        print("[Start Channel.Add()]")
        if channle in self.List:
            #已新增過的就直接return
            print("return False")
            return False
        else:
            self.List.append(channle)
            await self.Save()
            print("return True")
            return True
    
    #刪除channle,並save至json 
    async def delete(self, channle:int):
        print("[Start Channel.delete()]")
        if channle in self.List:
            self.List.remove(channle)
            await self.Save()
            print("return True")
            return True
        else:
            #不存在清單內的就直接return
            print("return False")
            return False
        
List = Channel()