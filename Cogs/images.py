import discord 
from discord.ext import commands
import os
import DiscordUtils
import random
from PIL import Image,ImageFont,ImageDraw
from io import BytesIO

class images(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print("image commands loaded")
        
  
    @commands.command()
    async def wanted(self,ctx,user:discord.Member = None):
        if user == None:
            user = ctx.author
            await ctx.send("you didnt mention anyone, so you are the one who is wanted now!! XD")
        wanted = Image.open("Images\wanted.jpg")
        asset = user.avatar_url_as(size = 128)
        data = BytesIO(await asset.read())
        profile = Image.open(data)
        profile = profile.resize((244,242))
        wanted.paste(profile,(76,193))
        wanted.save("profile.jpg")
        
        await ctx.send(file = discord.File("profile.jpg"))
    @commands.command()
    async def slap(self,ctx,user:discord.Member = None):
        if user == None:
            await ctx.send("Mention anyone to slap")
        else:
            slap = Image.open("Images\slap.jpg")
            
            asset = user.avatar_url_as(size = 128)
            assets = ctx.author.avatar_url_as(size = 128)
            
            
            
            data = BytesIO(await asset.read())
            datas = BytesIO(await assets.read())
            
            profile = Image.open(data)
            profiles = Image.open(datas)
            profile = profile.resize((210,246))
            profiles = profiles.resize((151,204))
            slap.paste(profiles,(388,222))
            slap.paste(profile,(123,304))
            slap.save("profile.jpg")
            await ctx.send(file = discord.File("profile.jpg"))
    @commands.command()
    async def dead(self,ctx,user:discord.Member = None):
        if user == None:
            await ctx.send("Mention anyone to slap")
        else:
            slap = Image.open("Images\deadlol.jpg")
            
            asset = user.avatar_url_as(size = 128)
            assets = ctx.author.avatar_url_as(size = 128)
            
            
            
            data = BytesIO(await asset.read())
            datas = BytesIO(await assets.read())
            
            profile = Image.open(data)
            profiles = Image.open(datas)
            
            profile = profile.resize((68,62))
            profiles = profiles.resize((50,43))
            
            slap.paste(profiles,(139,94))
            slap.paste(profile,(41,66))
            
            slap.save("profile.jpg")
            await ctx.send(file = discord.File("profile.jpg"))

def setup(bot):
    bot.add_cog(images(bot))