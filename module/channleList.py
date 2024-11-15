import asyncio
import json
import os

class Channel:
    def __init__(self):
        self.List = []
        
    async def load(self):
        if os.path.isfile("./data/channle.json"):
            with open("./data/channle.json",mode="r",encoding="utf8") as channleFile:
                self.List = json.load(channleFile)
        else:
            with open("./data/channle.json",mode="w",encoding="utf8") as channleFile:
                json.dump(self.List, channleFile)
                
    async def add(self, channle:int):
        if channle in self.List:
            return False
        else:
            self.List.append(channle)
            with open("./data/channle.json",mode="w",encoding="utf8") as channleFile:
                    json.dump(self.List, channleFile)
            return True
            
    async def delete(self, channle:int):
        if channle in self.List:
            self.List.remove(channle)
            with open("./data/channle.json",mode="w",encoding="utf8") as channleFile:
                    json.dump(self.List, channleFile)
            return True
        else:
            return False
    
    async def display(self):
        print(len(self.List))
        print(self.List)
        
List = Channel()