import discord
import psutil
import datetime
import requests
import json
from prettytable import PrettyTable
from bs4 import BeautifulSoup
from typing import Optional
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from core.classes import Cog_Extension
from tabulate import tabulate




class Slash(Cog_Extension):

    @app_commands.command(name = "info", description = "主機詳細資料!")
    async def info(self, interaction: discord.Interaction):
        cpu_percent = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        # 回覆使用者的訊息        
        embed = discord.Embed(title=f"主機詳細資料", description="", color=0x00ff00)
        embed.add_field(name="CPU使用率", value=f"{cpu_percent}", inline=True)
        embed.add_field(name="記憶體使用情況：", value=f"{mem.used / 1024 / 1024 / 1024:.2f} GB / {mem.total / 1024 / 1024 / 1024:.2f} GB", inline=True)
        embed.add_field(name="", value="", inline=False)
        embed.add_field(name="磁盤使用情況：", value=f"{disk.used / 1024 / 1024 / 1024:.2f} GB / {disk.total / 1024 / 1024 / 1024:.2f} GB", inline=True)
        embed.add_field(name="主機開機時間 : ", value=f"{time}", inline=True)

        # 发送嵌入式消息
        
        await interaction.response.send_message(embed=embed)

    # 參數: Optional[資料型態]，參數變成可選，可以限制使用者輸入的內容
    @app_commands.command(name = "say", description = "大聲說出來")
    @app_commands.describe(name = "輸入人名", text = "輸入要說的話")
    async def say(self, interaction: discord.Interaction, name: str, text: Optional[str] = None):
        if text == None:
            text = "。。。"
        await interaction.response.send_message(f"{name} 說 「{text}」")

    # @app_commands.choices(參數 = [Choice(name = 顯示名稱, value = 隨意)])
    @app_commands.command(name="mschedule", description="一軍月份賽程表")
    @app_commands.describe(m="選擇月份")
    @app_commands.choices(
        m=[
            Choice(name="4月", value="2023_04"),
            Choice(name="5月", value="2023_05"),
            Choice(name="6月", value="2023_06"),
            Choice(name="7月", value="2023_07"),
            Choice(name="8月", value="2023_08"),
            Choice(name="9月", value="2023_09"),
            Choice(name="10月", value="2023_10"),
        ]
    )
    async def mschedule(self, interaction: discord.Interaction, m: str):
        try:
            if m in self.cache:
                image = self.cache[m]
            else:
                with open(f"image/{m}.png", "rb") as f:
                    image = discord.File(f, f"{m}.png")

            if m == "2023_04":
                embed = discord.Embed(title=f"一軍{m}月份賽程表", description=f"以下是{m}補賽的日期", color=0x00ff00)
                embed.add_field(name="日期", value="2023/04/24", inline=True)
                embed.add_field(name="場次", value="G29", inline=True)
                embed.add_field(name="比賽", value="富邦悍將 VS 味全龍", inline=True)
                embed.add_field(name="原定日期", value="2023/04/19", inline=True)
                embed.add_field(name="時間", value="16:35", inline=True)
                embed.add_field(name="地點", value="天母棒球場", inline=True)
                embed.add_field(name="\u200b", value="\u200b", inline=False)
                embed.add_field(name="日期", value="2023/05/15", inline=True)
                embed.add_field(name="場次", value="G30", inline=True)
                embed.add_field(name="比賽", value="樂天桃猿 VS 中信兄弟", inline=True)
                embed.add_field(name="原定日期", value="2023/04/19", inline=True)
                embed.add_field(name="時間", value="16:35", inline=True)
                embed.add_field(name="地點", value="洲際棒球場", inline=True)
                embed.set_image(url=f"attachment://{m}.png")
            else:
                embed = discord.Embed(title=f"一軍{m}月份賽程表", description="", color=0x00ff00)
                embed.set_image(url=f"attachment://{m}.png")
            await interaction.response.send_message(embed=embed, file=image)
        except Exception as e:
            await interaction.response.send_message(f"發生錯誤：{str(e)}")



    @app_commands.command(name = "live", description = "中華職棒轉播平台")
    async def live(self, interaction: discord.Interaction):
        # 回覆使用者的訊息
         with open('image/schedule.jpg', 'rb') as f:
            image = discord.File(f,"schedule.jpg")
            await interaction.response.send_message(file=image)

    @app_commands.command(name="todayschedule", description="中華職棒賽程")
    async def todayschedule(self, interaction: discord.Interaction):
        date = datetime.date.today().strftime("%Y%m%d")
        url = f'https://www.playsport.cc/livescore.php?aid=6&gamedate={date}&mode=1'
        schedule_content = requests.get(url)
        soup = BeautifulSoup(schedule_content.text, 'html.parser')
        team = soup.find_all('div', {'class': 'AllGamesList'}) 
        time = soup.find_all('td', {'class': 'team_cinter'})
        if len(team) == 0:
            # 如果當天沒有比賽
            embed = discord.Embed(title=f"中華職棒 {date}", description="當天沒有比賽", color=0x00ff00)
        else:
        # 如果有比賽
            embed = discord.Embed(title=f"中華職棒 {date}", description=f"今天有{len(team)}場賽事", color=0x00ff00)
        for i, game in enumerate(team):
            game_text = game.text.strip()
            game_time = time[i].text.strip()  # 每個比賽對應的時間在time變數中出現兩次，所以需要選取對應的那一個
            embed.add_field(name="對戰隊伍", value=f"{game_text}", inline=True)
            embed.add_field(name="比賽時間", value=f"{game_time}", inline=True)
            embed.add_field(name="網路轉播", value=f"[CPBLTV](https://hamivideo.hinet.net/hamivideo/main/606.do)", inline=True)
        embed.set_footer(text="資料來源：中華職棒官網", icon_url="")    

        await interaction.response.send_message(embed=embed)


    @app_commands.command(name = "season", description = "中華職棒隊伍戰績")
    async def season(self, interaction: discord.Interaction):
        url = "https://www.fubonguardians.com/content/fixtures/Records"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # 尋找包含上半季賽事紀錄的表格
        table = soup.find("table", {"class": "table table-keep-all table-fbg-primary table-striped text-center mb-0"})

    # 從表格中抓取資料
        rows = table.find_all("tr")
        data = []
        for row in rows:
            cols = row.find_all("td")
            cols1 = row.find_all("th")
            cols = [col.text.strip()[:10] for col in cols]  # Extract only the first 5 characters
            cols1 = [col1.text.strip()[:6] for col1 in cols1]  # Extract only the first 4 characters
            data.append(cols1 + cols)

        table = PrettyTable()
        table.field_names = ["Team"] + data[0][1:]
        for row in data[1:]:
            table.add_row(row)

        await interaction.response.send_message(f"```\n{table}\n```")


    @app_commands.command(name = "websites", description = "隊伍官網連結")
    async def websites(self, interaction: discord.Interaction):
        # 回覆使用者的訊息
        embed = discord.Embed(title=f"六隊的官網連結", description="", color=0x00ff00)
        embed.add_field(name="中信兄弟BROTHERS", value="[中信官網](http://www.brothers.tw/)", inline=True)
        embed.add_field(name="統一7-ELEVEn獅U-LIONS", value="[統一官網](https://www.uni-lions.com.tw/)", inline=True)
        embed.add_field(name="樂天桃猿MONKEYS", value="[樂天官網](https://monkeys.rakuten.com.tw/)", inline=True)
        embed.add_field(name="富邦悍將GUARDIANS", value=f"[富邦悍將官網](https://www.fubonguardians.com/)", inline=True)
        embed.add_field(name="味全龍DRAGONS : ", value=f"[味全龍官網](https://www.wdragons.com/CWS)", inline=True)
        embed.add_field(name="台鋼雄鷹TSG HAWKS", value=f"[目前還沒]()", inline=True)

        await interaction.response.send_message(embed=embed)


    @app_commands.command(name = "ls", description = "即時比分")
    async def ls(self, interaction: discord.Interaction):
        # 回覆使用者的訊息
        date = datetime.date.today().strftime("%Y%m%d")
        url = f"https://www.playsport.cc/livescore.php?aid=6&gamedate={date}&mode=1&ui=m2"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        team_scores = soup.find_all('div', {'class': 'gamelist__team'})
        todayurl = f'https://www.playsport.cc/livescore.php?aid=6&gamedate={date}&mode=1'
        today_content = requests.get(todayurl)
        today_soup = BeautifulSoup(today_content.text, 'html.parser')
        team = today_soup.find_all('div', {'class': 'AllGamesList'}) 
        time = today_soup.find_all('td', {'class': 'team_cinter'})


        # embed.add_field(name="目前還在開發中", value=f"", inline=True)

        if not team_scores:
            embed = discord.Embed(title=f"{date}", description=f"今天沒有比賽", color=0x00ff00)
            print("今天沒有比賽")
        else:
            embed = discord.Embed(title=f"{date} 即時比分", description=f"比分可能會更新的比較慢請見諒", color=0x00ff00)
            for team_score in team_scores:
                team_names = team_score.find_all('div', {'class': 'team_name'})
                team_scores = team_score.find_all('div', {'class': 'team_score'})
                for i in range(0, len(team_names), 2):
                    teamname1 = team_names[i].get_text().strip()[:2]
                    teamscore1 = team_scores[i].get_text().strip()
                    if i + 1 < len(team_names):
                        teamname2 = team_names[i+1].get_text().strip()[:2]
                        teamscore2 = team_scores[i+1].get_text().strip()
                        embed.add_field(name=f"{teamname1}VS{teamname2}", value=f"```{teamscore1}  -  {teamscore2}```", inline=True)
                    else:
                        embed.add_field(name=f"{teamname1}", value=f"{teamscore1}", inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=False) # 加入空白字符來製造分隔線
            for i, game in enumerate(team):
                game_text = game.text.strip()
                game_time = time[i].text.strip()  # 每個比賽對應的時間在time變數中出現兩次，所以需要選取對應的那一個
                embed.add_field(name="對戰隊伍", value=f"{game_text}", inline=True)
                embed.add_field(name="比賽時間", value=f"{game_time}", inline=True)
                embed.add_field(name="網路轉播", value=f"[CPBLTV](https://hamivideo.hinet.net/hamivideo/main/606.do)", inline=True)
            
            # for i in range(len(team_names)):
            #     team_name = team_names[i].text.strip()
            #     score = team_scores[i].text.strip()
            #     embed.add_field(name=f"{team_name}", value=f"{score}", inline=True)
            #     print(f"{team_name}: {score}")
        


        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name = "gamesno", description = "查詢場次資料 範例 /gamesno 012 (不及時更新)")
    @app_commands.describe(game_id = "比賽代號 例:01、012")
    async def gamesno(self, interaction: discord.Interaction, game_id: str):
        try:
            with open("json/gameSno.json", "r" ,encoding='utf-8') as f:
                data = json.load(f)

            def get_game_data(game_id):# 定義一個函數，用於從data中獲取特定game_id的遊戲資料
                for obj in data:
                    if obj["game"] == game_id:
                        return obj

            game_data = get_game_data(game_id) # 使用剛定義的函數來獲取特定遊戲的資料
            if game_data is not None:# 如果成功找到遊戲資料，就建立一個discord.Embed物件來顯示資訊
                embed = discord.Embed(title=f"場次{game_id} null = 未知/未更新", description=f"比賽地點: {game_data['Ballpark']}", color=0x00ff00)
                embed.add_field(name=f"對戰隊伍", value=f"{game_data['team']}", inline=True)
                embed.add_field(name=f"比分", value=f"{game_data['score']}", inline=True)
                embed.add_field(name="", value="", inline=False)
                embed.add_field(name=f"觀眾人數", value=f"{game_data['viewership']}", inline=True)
                embed.add_field(name=f"MVP", value=f"{game_data['MVP']}", inline=True)
                embed.add_field(name=f"比賽時間", value=f"{game_data['Game_time']}", inline=True)
                await interaction.response.send_message(embed=embed)# 使用interaction.response.send_message()方法發送消息
            else:# 如果找不到遊戲資料，就發送一個錯誤消息
                await interaction.response.send_message(f"找不到場地 ID 為 {game_id} 的資料")
        except Exception as e: # 如果出現異常，就在控制台中顯示錯誤消息，並向用戶發送一個錯誤消息
            print(e)
            await interaction.response.send_message("出现异常，请稍后重试。")

    @app_commands.command(name = "goal", description = "想要更新的目標")
    async def goal(self, interaction: discord.Interaction):
        # 回覆使用者的訊息
        embed = discord.Embed(title=f"更新的目標", description="", color=0x00ff00)
        embed.add_field(name="1.方便性", value="可在狀態中顯示今天有幾場比賽", inline=False)
        embed.add_field(name="2.個人能力", value="能讓我的python能力更好，製造更好的系統", inline=False)
        embed.add_field(name="3.便利使用", value="能讓機器人自動化查詢比賽資料", inline=False)
        embed.add_field(name="4.美觀性", value="能讓表達方式更簡潔", inline=False)

        await interaction.response.send_message(embed=embed)
    

    # @app_commands.command(name = "helpmenu", description = "機器人所有指令")
    # async def helpmenu(self, interaction: discord.Interaction):
    #     # 回覆使用者的訊息
    #     embed = discord.Embed(title=f"指令表", description="", color=0x00ff00)
    #     embed.add_field(name="/todayschedule ", value="今天的賽程(一軍)", inline=True)
    #     embed.add_field(name="/mschedule", value="月份賽程表(一軍)", inline=True)
    #     embed.add_field(name="/season ", value="各隊戰績表", inline=True)
    #     embed.add_field(name="/gamesno", value="查詢場次資料(固定週五更新)", inline=False)
    #     embed.add_field(name="/live", value="各隊轉播平台", inline=True)
    #     embed.add_field(name="/websites ", value="各隊的官網", inline=True)
    #     embed.add_field(name="/ls ", value="即時比分(開發中)", inline=True)


    #     await interaction.response.send_message(embed=embed)


    @app_commands.command(name = "stadium", description = "台灣所有球場")
    async def stadium(self, interaction: discord.Interaction):
        # 回覆使用者的訊息
        url = 'https://dev.cpbl.com.tw/field'
        stadium_content = requests.get(url)
        soup = BeautifulSoup(stadium_content.text, 'html.parser')
        stadiums = soup.find_all('div', {'class': 'item'})

        # 將球場資訊整理成表格形式
        table_header = ["地址", "球場名稱"]
        table_data = []
        for stadium in stadiums:
            name = stadium.find("dt").get_text().strip()
            address_list = stadium.find_all("dd")
            address = " ".join([addr.get_text().strip() for addr in address_list])
            table_data.append([name, address])

        # 將表格資料加入嵌入式物件
        embed = discord.Embed(title="台灣所有球場", description="以下是台灣各地的棒球場地列表", color=0x00ff00)
        embed.add_field(name=" ", value="```" + tabulate(table_data, headers=table_header, tablefmt="simple") + "```", inline=False)




        await interaction.response.send_message(embed=embed)
async def setup(bot):
    await bot.add_cog(Slash(bot))
