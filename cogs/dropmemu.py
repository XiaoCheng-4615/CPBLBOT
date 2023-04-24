import discord
import asyncio
from datetime import datetime
from discord import ButtonStyle, app_commands
from core.classes import Cog_Extension

class Selectlist(discord.ui.Select):
   def __init__(self):
        options = [
            discord.SelectOption(label="d", emoji="d", description="d"),
            discord.SelectOption(label="d", emoji="d", description="d"),
            discord.SelectOption(label="d", emoji="d", description="d")
        ]
        super().__init__(placeholder="請選擇，以下設定請全部設定完畢...", options=options)
        self.selected_options = set()

   async def callback(self, interaction: discord.Interaction):
      if self.selected_options and self.selected_options.pop() == self.values[0]:
            # 如果第一个选项已经被选择过了，就不能再选择
            await interaction.response.send_message("你已经选择过此选项了。", ephemeral=True)
      else:
            # 记录已选择的选项
            self.selected_options.add(self.values[0])
            selected_option = self.values[0]
            if selected_option == "倒數時間設定":
                # 弹出输入框，要求用户输入倒计时的时间
                await interaction.response.send_message("請輸入倒計時的時間：", ephemeral=True)
                try:
                    # 等待用户的输入
                    response = await self.bot.wait_for("message", check=lambda m: m.author == interaction.user and m.channel == interaction.channel)
                    # 处理用户的输入
                    countdown_time = int(response.content)
                    await response.channel.send(f"已将倒计时时间设为 {countdown_time} 秒。")
                except asyncio.TimeoutError:
                    # 如果用户没有在规定时间内输入，就取消操作
                    await interaction.response.send_message("你没有在规定时间内输入，操作已取消。", ephemeral=True)
            elif selected_option == "發送頻道設定":
                # 创建一个新的消息，要求用户选择发送投票消息的频道
                await interaction.response.send_message("請选择投票消息要发送的频道：", ephemeral=True)
            elif selected_option == "投票人數起始值設定":
                # 创建一个新的消息，要求用户输入本次投票需要的最少投票人数
                await interaction.response.send_message("請输入本次投票需要的最少投票人数：", ephemeral=True)

class FeedbackModal(discord.ui.Modal, title="設定投票機選項"):
   fb_title = discord.ui.TextInput(
      style = discord.TextStyle.short,
      label = "投票標題",
      required = True,
      placeholder = "請輸入投票的標題"
   ) 

   message = discord.ui.TextInput(
      style = discord.TextStyle.long,
      label = "投票內容說明",
      required = True,
      max_length = 500,
      placeholder = "請輸入投票的內容"
   )

   options = []

   async def on_submit(self, interaction: discord.Interaction):
      self.options.append(self.fb_title.value)
      self.options.append(self.message.value)
      # embed = discord.Embed(title=f"{self.options[0]}", description=self.options[1], color=discord.Color.yellow())
      # embed.set_author(name=interaction.user.name)
      view = discord.ui.View()
      view.add_item(Selectlist())
      await interaction.response.edit_message(content="請設定完以下按鈕的所有設定，來完成啟動投票", view=view)

      
   async def on_error(self, interaction: discord.Interaction, error):
      await interaction.response.send_message("錯誤")

class dropmenu(Cog_Extension):
   @app_commands.command(name="test", description="投票機測試")
   async def poll(self, interaction: discord.Interaction):
      button = discord.ui.Button(label="點我開始設定投票機選項", style=ButtonStyle.green, emoji="⚙")
      # await interaction.response.send_message("請按下按鈕")

      async def button_callback(interaction: discord.Interaction):
         await interaction.response.send_modal(feedback_modal)

      feedback_modal = FeedbackModal()

      button.callback = button_callback

      view = discord.ui.View()
      view.add_item(button)

      await interaction.response.send_message("請按下方的按鈕", view=view)
      
async def setup(bot):
   await bot.add_cog(dropmenu(bot))
