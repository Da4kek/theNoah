import discord
from discord.ext import commands
import DiscordUtils
import paginator
import asyncio
import json
import time
import random

def  convert(time):
    
    pos = ['s','m','h','d']
    time_dict = {"s":1,"m":60,"h":3600,"d":3600*24}
    unit = time[-1]
    
    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2
    return val * time_dict[unit]



class giveaway(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
    @commands.Cog.listener()    
    async def on_ready(self):
        print('giveaway command loaded')
        

        
    @commands.command()
    @commands.has_permissions(manage_channels =True)
    async def giveaway(self,ctx):
        await ctx.send("Let's start with this giveaway! all you need to do is answer these questions within 15 secs!")
        questions = ["**Which channel should the giveaway be hosted in?**",
                    "**What should be the duration of the giveaway? (s|m|h|d)**",
                    "**What is the prize of the giveaway??**"]
        answers = []
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        for i in questions:
            await ctx.send(i)
            try:
                msg = await self.bot.wait_for("message",timeout = 15.0,check=check)
            except asyncio.TimeoutError:
                await ctx.send("`You didnt answer in 15 secs please try again!`")
                return
            else:
                answers.append(msg.content)        
        try:
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(f"`mention the channel properly!. Try like this {ctx.channel.mention} next time.`")
            return
        channel = self.bot.get_channel(c_id)
        time = convert(time = answers[1])
        if time == -1:
            await ctx.send(f"`you didnt answer the time with proper unit. use (s|m|h|d)`")
            return
        elif time == -2:
            await ctx.send(f"`the time must be a whole number please enter the number as a whole!`")
            return
        prize = answers[2]
        await ctx.send(f"**the Giveaway will be in {channel.mention} and will last for {answers[1]}")
        embed = discord.Embed(title = "Giveaway!",description = f"{prize}",color = ctx.author.color)
        embed.add_field(name = "Hosted by:",value = ctx.author.mention)
        embed.set_footer(text = f"Ends {answers[1]} from now!")
        my_msg = await channel.send(embed = embed)

        await my_msg.add_reaction("🎉")
        await asyncio.sleep(time)
        
        new_msg = await channel.fetch_message(my_msg.id)

        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        print(users)

        winner = random.choice(users)
        await channel.send(f"Congratulations!! {winner.mention} won {prize}")
        
    @commands.command()
    @commands.has_permissions(manage_channels= True)
    async def reroll(self,ctx,channel : discord.TextChannel, id_ : int,prize:str):
        try: 
            new_msg = await channel.fetch_message(id_)
        except: 
            await ctx.send("`the id entered incorrectly!`")
            return
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(commands.user))
        
        winner = random.choice(users)
        await channel.send(f"Congratulations!! {winner.mention} won {prize}")
        

def setup(bot):
    bot.add_cog(giveaway(bot))