import discord 
from discord.ext import commands
import os
import DiscordUtils
import random
from PIL import Image,ImageFont,ImageDraw
from io import BytesIO
from aiohttp import request
import asyncio
import aiohttp
import json


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
            
            
            
    
    @commands.command()
    async def fact(self, ctx, animal: str):
            if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
                fact_url = f"https://some-random-api.ml/facts/{animal}"
                image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

                async with request("GET", image_url, headers={}) as response:
                    if response.status == 200:
                        data = await response.json()
                        image_link = data["link"]

                    else:
                        image_link = None

            async with request("GET", fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = discord.Embed(title=f"{animal.title()} fact",
                                    description=data["fact"],
                                    colour=ctx.author.colour)
                    if image_link is not None:
                        embed.set_image(url=image_link)
        
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"API returned a {response.status} status.")
    @commands.command()
    async def searchdocs(self,ctx,search: str):
        url = f''      
                




def setup(bot):
    bot.add_cog(fun(bot))