import discord 
from discord.ext import commands
import os
import DiscordUtils
import random
from PIL import Image,ImageFont,ImageDraw
from io import BytesIO

class fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print("fun commands loaded")
        
    @commands.command()
    async def roll(self,ctx, dice:int=3):
        if dice > 20:
            await ctx.send(f'Sorry, but i don\'t have {dice} dice')
            return
        if dice < 1:
            await ctx.send(f'Sorry, but i don\'t have {dice} die')
            return
        a = []
        for x in range(dice):
            a.append(str(random.randint(0, 10)))
        await ctx.send('You Rolled: \n`' + (', '.join(a)) + '`')  
    @commands.command()
    async def allcommands(self,ctx):
        await ctx.send(len(bot.commands))
    @commands.command()
    async def kill(self,ctx, member:discord.Member=None, *, reason:str=None):
        if member == None or member == ctx.author:
            await ctx.send(f'{ctx.author.mention} commited suicide')
            return
        if reason == None:
            await ctx.send(f'{ctx.author.mention} killed {member.mention}')
        elif reason != None:
            await ctx.send(f'{ctx.author.mention} killed {member.mention} for {reason}') 
    @commands.command()
    async def count(self,ctx, ending=100):
        for x in range(ending + 1):
            await ctx.send(x)

def setup(bot):
    bot.add_cog(fun(bot))