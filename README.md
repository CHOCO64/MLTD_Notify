# MLTD 活動提醒 Discord 機器人

## 關於這個機器人
這個機器人是手機遊戲《アイドルマスター ミリオンライブ！ シアターデイズ》的Discord專用活動提醒機器人，會在有打活動曲活動時,自動發提醒出來。
活動資訊的獲取是依賴於[matsurihi API](https://api.matsurihi.me/docs/)

## 前置作業

```
python3 -m pip install -U discord.py
python3 -m pip install -U APScheduler
```

## 設定檔
config.json
```json
{
    "botToken": ""
}
```
只要填入機器人的token就好了

## 部署方法
在Linux server上執行
```
nohup python3 -u bot.py >log.log 2>&1 &
```
會產生log.log的log檔

##存放資料說明
下列的檔案都是在機器人執行時會自動產生的檔案

data/channle.json <=註冊要讓機器人發提醒的頻道
data/mltd.json <=目前最新的活動資料

## 相依套件

| 套件名稱 |
| --- |
| [discord.py](https://pypi.org/project/discord.py/) |
| [APScheduler](https://pypi.org/project/APScheduler/) |
