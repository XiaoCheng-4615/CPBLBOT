import os
import asyncio
import discord
import requests
import datetime
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
    # 缓存数据和缓存更新时间
    cached_data = None
    cache_expiration_time = None
    
    while True:
        # 检查缓存是否过期
        if not cache_expiration_time or datetime.datetime.now() >= cache_expiration_time:
            # 过期或者没有缓存，进行API调用和HTTP请求，并更新缓存
            date = datetime.date.today().strftime("%Y%m%d")
            url = f'https://www.playsport.cc/livescore.php?aid=6&gamedate={date}&mode=1'
            schedule_content = requests.get(url)
            soup = BeautifulSoup(schedule_content.text, 'html.parser')
            team = soup.find_all('div', {'class': 'AllGamesList'})
            
            # 更新缓存数据和缓存更新时间
            cached_data = team
            cache_expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
        
        # 根据缓存数据更新Discord状态
        if len(cached_data) == 0:
            await bot.change_presence(activity=discord.Game(f'今天沒有比賽'), status=discord.Status.online)
        else:
            await bot.change_presence(activity=discord.Game(f'今天有 {len(cached_data)} 場比賽'), status=discord.Status.online)
        
        # 更新日期和其他信息的Discord状态
        date = datetime.date.today().strftime("%Y%m%d")
        await bot.change_presence(activity=discord.Game(f'今天日期: {date}'), status=discord.Status.online)
        await asyncio.sleep(3) # 更改動態的秒數
        await bot.change_presence(activity=discord.Game(f'⚾中華職棒(非官方) | PHACS 製作'), status=discord.Status.online)
        await asyncio.sleep(3) # 更改動態的秒數

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
