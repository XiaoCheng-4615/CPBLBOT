import os
import asyncio
import discord
import requests
import datetime
import sched
import time
import subprocess
from bs4 import BeautifulSoup
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "$", intents = intents)


# 當機器人完成啟動時
@bot.event
async def on_ready():
    # 同步所有的斜線指令
    slash_commands = await bot.tree.sync()

    # 創建 status_task
    bot.loop.create_task(status_task())

    # 印出登入身份以及載入的斜線指令數量
    print(f"目前登入身份 --> {bot.user}")
    print(f"已載入 {len(slash_commands)} 個斜線指令")

async def status_task():
    while True:
            date = datetime.date.today().strftime("%Y%m%d")
            url = f'https://www.playsport.cc/livescore.php?aid=6&gamedate={date}&mode=1'
            schedule_content = requests.get(url)
            soup = BeautifulSoup(schedule_content.text, 'html.parser')
            team = soup.find_all('div', {'class': 'AllGamesList'})
            time = soup.find_all('td', {'class': 'team_cinter'})
        
            # 根据缓存数据更新Discord状态
            if len(team) == 0:
                game_status = [
                    {'type': 'Playing', 'name': f'今天日期: {date}'},
                    {'type': 'Listening', 'name': '今天沒有比賽'},
                    {'type': 'Listening', 'name': '⚾中華職棒(非官方) | PHACS 製作'},
                ]
            elif len(team) > 1:
                game_status = [
                    {'type': 'Playing', 'name': f'今天日期: {date}'},
                    {'type': 'Playing', 'name': f'今天有 {len(team)} 場比賽'},
                    {'type': 'Playing', 'name': f'{team[0].text.strip()}, {time[0].text.strip()}'},
                    {'type': 'Playing', 'name': f'{team[1].text.strip()}, {time[1].text.strip()}'},
                    {'type': 'Listening', 'name': '⚾中華職棒(非官方) | PHACS 製作'},
                ]
            else:
                game_status = [
                    {'type': 'Playing', 'name': f'今天日期: {date}'},
                    {'type': 'Playing', 'name': f'今天有 {len(team)} 場比賽'},
                    {'type': 'Playing', 'name': f'{team[0].text.strip()}, {time[0].text.strip()}'},
                    {'type': 'Listening', 'name': '⚾中華職棒(非官方) | PHACS 製作'},
                ]

            current_status = 0
            while True:
                game = discord.Game(name=game_status[current_status]['name'], type=game_status[current_status]['type'])
                await bot.change_presence(activity=game)
                current_status = (current_status + 1) % len(game_status)
                await asyncio.sleep(5)  # 状态循环时间


# 載入指令程式檔案
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")

# 卸載指令檔案
@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")

# 重新載入程式檔案
@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")

# 一開始bot開機需載入全部程式檔案
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            
async def main():
    async with bot:
        await load_extensions()
        await bot.start("MTA5NDQwNjc0MzE5MjI1MjUwOA.G8d80j.nt8umCKrbi-wC0zcnT4P6BXL-ekysjYn83Hz10")

# 確定執行此py檔才會執行
if __name__ == "__main__":
    asyncio.run(main())

def restart_bot():
    # 停止機器人
    subprocess.run(["taskkill", "/F", "/IM", "python.exe", "/T", "/FI", 'WINDOWTITLE eq python bot.py'])
    # 啟動機器人
    subprocess.Popen(["python", "bot.py"])

# 建立事件調度程序
scheduler = sched.scheduler(time.time, time.sleep)

# 計劃第一次執行
today = time.localtime()
runtime = time.mktime((today.tm_year, today.tm_mon, today.tm_mday, 0, 0, 0, 0, 0, -1))
if time.time() > runtime:
    runtime += 86400  # 如果當前時間已經過了今天的 00:00，則將重啟時間推到明天的 00:00
    print('下次重啟時間')
scheduler.enterabs(runtime, 1, restart_bot)

# 計劃下一次執行
scheduler.enter(86400, 1, restart_bot)

# 啟動事件調度程序
scheduler.run()
