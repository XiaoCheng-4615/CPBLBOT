import os
import asyncio
import discord
import psutil
import requests
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
        use = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        await bot.change_presence(activity=discord.Game(f'CPU使用量 ' + str(use) +  ' %'), status=discord.Status.online)
        await asyncio.sleep(3) # 更改動態的秒數
        await bot.change_presence(activity=discord.Game(f'RAM使用量：{ram.used / 1024 / 1024 / 1024:.2f} GB / {ram.total / 1024 / 1024 / 1024:.2f} GB\n'), status=discord.Status.online)
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
