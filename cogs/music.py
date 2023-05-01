import discord
from discord.ext import commands
import youtube_dl
from core.classes import Cog_Extension

class Music(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, url):
        guild = ctx.guild
        voice_client = guild.voice_client

        if not voice_client:
            await ctx.author.voice.channel.connect()
            voice_client = guild.voice_client

        with youtube_dl.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            voice_client.play(discord.FFmpegPCMAudio(URL), after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(Music(bot))

