# This example requires the 'message_content' privileged intent to function.

import discord
from discord.ext import commands
from core.classes import Cog_Extension
from discord import app_commands
from discord.app_commands import Choice
# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice
class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='todayschedule', description='今天的賽程(一軍)', emoji='🟥'),
            discord.SelectOption(label='mschedule', description='月份賽程表(一軍)', emoji='🟩'),
            discord.SelectOption(label='season', description='各隊戰績表', emoji='🟦'),
            discord.SelectOption(label='gamesno', description='查詢場次資料(固定週五更新)', emoji='🟦'),
            discord.SelectOption(label='live', description='各隊轉播平台', emoji='🟦'),
            discord.SelectOption(label='websites', description='各隊的官網', emoji='🟦'),
            discord.SelectOption(label='ls', description='即時比分(開發中)', emoji='🟦'),

        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='⚾指令教學', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        option = self.values[0]  # 取得使用者所選擇的選項
        option_obj = next((opt for opt in self.options if opt.label == option), None)  # 取得選項對應的 SelectOption 物件
        if option_obj is not None:
            embed = discord.Embed(title=f"{option}", description=f"{option_obj.description}", color=0x00ff00)
            embed.set_author(name="中華職棒(非官方)", url="https://www.cpbl.com.tw")
            embed.set_image(url='https://www.cpbl.com.tw/theme/common/images/project/logo_new.png')
        else:
            embed = discord.Embed(title=f"{option}", description=f"沒有詳細說明", color=0x00ff00)
            embed.set_author(name="中華職棒(非官方)", url="https://www.cpbl.com.tw/theme/common/images/project/logo_new.png")
        await interaction.response.send_message(embed=embed)


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())


class DropdownMenu(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        """"""

        # Create the view containing our dropdown
        view = DropdownView()

        # Sending a message containing our view
        embed = discord.Embed(title=f"CPBL中華職棒(非官方)", description="我的目標是可以在discord，直接查詢今天的賽事或者一些資訊", color=0x00ff00)
        await ctx.send(embed=embed , view=view)

    @app_commands.command(name = "help", description = "指令列表")
    async def info(self, interaction: discord.Interaction):
        view = DropdownView()
        # 回覆使用者的訊息        
        embed = discord.Embed(title=f"CPBL中華職棒(非官方)", description="我的目標是可以在discord，直接查詢今天的賽事或者一些資訊", color=0x00ff00)
        # 发送嵌入式消息
        
        await interaction.response.send_message(embed=embed , view=view)


async def setup(bot):
    await bot.add_cog(DropdownMenu(bot))
