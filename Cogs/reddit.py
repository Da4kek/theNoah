import discord
from discord.ext import commands
import praw
import os
import random
reddit = praw.Reddit(client_id = "5T3myV5BQSWmvQ",
                     client_secret = "j2NeTcoFNEYyV6hCp6erdk1h3cO7vQ",
                     username = "nocopyrights101",
                     password = "Myindian@123",
                     user_agent = "NoahBot")



class  memes(commands.Cog):
    def __init__(self,bot):
           self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print("reddit commands loaded")
    
    @commands.command()
    async def meme(self,ctx):
        subreddit = reddit.subreddit("memes")
        all_submission =[]
        
        top = subreddit.top(limit = 50)
        for submission in top:
            all_submission.append(submission)
        random_sub = random.choice(all_submission)
        name = random_sub.title
        url = random_sub.url
        embed = discord.Embed(title = name)
        embed.set_image(url = url)
        await ctx.send(embed = embed)    
        
    @commands.command()
    async def subreddit(self,ctx,sub : str = None):
        if(sub == None):
            await ctx.send("mention the subreddit!")
        else:
        
            subreddit = reddit.subreddit(sub)
            all_submission =[]
            
            top = subreddit.top(limit = 50)
            for submission in top:
                all_submission.append(submission)
            random_sub = random.choice(all_submission)
            name = random_sub.title
            url = random_sub.url
            embed = discord.Embed(title = name)
            embed.set_image(url = url)
            await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(memes(bot))        
        