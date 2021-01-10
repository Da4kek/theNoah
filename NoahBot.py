import discord 
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import json
import asyncio
from PIL import Image,ImageFont,ImageDraw
from io import BytesIO
import datetime
import mysql.connector
import DiscordUtils
import praw

def get_prefix(client,message):
    
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix = get_prefix)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')


bot.remove_command("help")
reddit = praw.Reddit(client_id = "5T3myV5BQSWmvQ",
                     client_secret = "j2NeTcoFNEYyV6hCp6erdk1h3cO7vQ",
                     username = "nocopyrights101",
                     password = "Myindian@123",
                     user_agent = "NoahBot")

os.chdir("C:\\Users\\anisr\\OneDrive\\Desktop\\NoahBot\\")
def convert(time):
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

async def get_bank_data():
    with open("mainbank.json",'r') as f:
        users = json.load(f)
    return users
    


async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['wallet'] = 0
        users[str(user.id)]['bank'] = 0
        
    with open("mainbank.json",'r+') as f:
        json.dump(users,f)
    return True



#############################################################################################################

@bot.event
async def on_guild_join(guild):


    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "noah"

    with open("prefixes.json", "w") as f:
        json.dump(prefixes,f)

#############################################################################################################
        
@bot.command()
@commands.has_permissions(administrator = True)
async def changeprefix(ctx, prefix):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes,f)    

    await ctx.send(f"The prefix was changed to {prefix}")

#############################################################################################################



@bot.command()
async def meme(ctx,subred = 'memes'):
    subreddit = reddit.subreddit(subred)
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

#############################################################################################################
    
@bot.command()
async def subreddit(ctx,subred = None):
    if(subred == None):
        await ctx.send("Enter the subreddit's name and try again")
    else:
    
        subreddit = reddit.subreddit(subred)
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

#############################################################################################################        

@bot.command()
@commands.has_permissions(manage_channels =True)
async def purge(ctx,amount = 5):
    await ctx.channel.purge(limit = amount)
    
filtered_words = ['fuck','FUCK','fck','sex','pussy','mf','motherfucker','bitch','ass','ASS','thefuck','wtf','WTF']
    
#############################################################################################################    

@bot.command()
async def help(ctx):
    embed1 = discord.Embed(color=ctx.author.color).add_field(name="**Moderations**",value = None)
    embed1.add_field(name = 'createchannel',value = 'creates a channel for you')
    embed1.add_field(name = 'deletechannel',value ='deletes a channel (give the name/id/mention the channel)')
    embed1.add_field(name = 'kick',value = 'kicks the member whom you mention')
    embed1.add_field(name = 'ban',value = 'bans the member whom you mention and wont allow him to join again unless unbanned')
    embed1.add_field(name = 'unban',value = 'unbans the member(give me the username with the code of the banned member)')
    embed1.add_field(name = 'automod',value = 'coming soon!')
    
    embed2 = discord.Embed(color=ctx.author.color).add_field(name="**Fun**",value = None)
    embed2.add_field(name = 'slap',value = 'mention a member to slap')
    embed2.add_field(name = 'dead',value = 'mention a member, and he is dead with your smile lol')
    embed2.add_field(name = 'wanted',value = 'mention a member whom you wanted to see him most wanted')
    embed2.add_field(name = 'roll',value='give me the sides and number of dices to use ;)')
    
    embed3 = discord.Embed(color=ctx.author.color).add_field(name="**Giveaway**",value = None)
    embed3.add_field(name = 'giveaway',value = "start a giveaway with some basic questions (be legit!)")
    
    embed4 = discord.Embed(color=ctx.author.color).add_field(name="**economy**",value = None)
    embed4.add_field(name='balance',value = 'to see how much do you have')
    embed4.add_field(name = 'beg',value = 'beg to get noacoins')
    embed4.add_field(name = 'shops',value = 'coming soon!')
    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
    paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⏪', "back")
    paginator.add_reaction('🔐', "lock")
    paginator.add_reaction('⏩', "next")
    paginator.add_reaction('⏭️', "last")
    embeds = [embed1, embed2, embed3,embed4]
    await paginator.run(embeds)




#############################################################################################################
    
@bot.command()
@commands.has_permissions(manage_channels =True)
async def giveaway(ctx):
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
            msg = await bot.wait_for("message",timeout = 15.0,check=check)
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
    channel = bot.get_channel(c_id)
    time = convert(answers[1])
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
    
    new_msg = await ctx.channel.fetch_message(my_msg.id)
    
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(bot.user))
    
    winner = random.choice(users)
    await channel.send(f"Congratulations!! {winner.mention} won {prize}")

#############################################################################################################
    
    
@bot.command()
@commands.has_permissions(manage_channels= True)
async def reroll(ctx,channel : discord.TextChannel, id_ : int,prize:str):
    try: 
        new_msg = await channel.fetch_message(id_)
    except: 
        await ctx.send("`the id entered incorrectly!`")
        return
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(bot.user))
    
    winner = random.choice(users)
    await channel.send(f"Congratulations!! {winner.mention} won {prize}")

#############################################################################################################

@bot.command()
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    wallet_amt = users[str(user.id)]['wallet']
    bank_amt = users[str(user.id)]['bank']
    embed = discord.Embed(title = f"{ctx.author.name}'s balance",color = discord.Color.red())
    embed.add_field(name = "Wallet balance",value = wallet_amt)
    embed.add_field(name = "Bank balance",value = bank_amt)
    await ctx.send(embed = embed)
    
#############################################################################################################


 
############################################################################################################# 
    
@bot.command()
async def beg(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author

    earnings = random.randrange(101)
    await ctx.send(f"**Someone gave you {earnings} noacoins!**")
    users[str(user.id)]['wallet'] += earnings
    with open("mainbank.json",'w') as f:
        users = json.dump(users,f)
    
#############################################################################################################    
@bot.event
async def on_ready():
    for guild in bot.guilds:
        print("{} logged in successfully \n".format(bot.user))
        print(f"{guild.name}(id: {guild.id})")
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild members:\n -  {members}')
    await bot.change_presence(activity=discord.Game(name = "playing on {} servers".format(len(bot.guilds))))
    await bot.change_presence(activity = discord.Streaming(name = "Streaming",url = "https://twitch.com"))
    await bot.change_presence(activity=discord.Activity(type = discord.ActivityType.listening,name = "Noah"))
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching,name = "How was Noah made"))
    
async def change_presence():
    await bot.wait_until_ready()
    status = ['Noah',f'on {len(bot.guilds)} servers | noah help','discord.py']
    while not bot.is_closed():
        status = random.choice(status)
        
        await bot.change_presence(activity=discord.Game(name = status))
        await asyncio.sleep(30)
bot.loop.create_task(change_presence())
        
    
 #############################################################################################################   
    
    
@bot.event
async  def on_member_join(member):
    channel = bot.get_all_channels()
    await channel.send(f"Welcome {member}! to {member.guild.name}!!")
    await member.create_dm()
    await member.dm_channel.send(f"Hi {member.name}, welcome to the {bot.guild.name} server!!")
    
#############################################################################################################    
    
@bot.event
async  def on_message(message):
    if message.author == bot.user:
        return
    sample_texts = ["Hello whatsup ??","you like me??","am developing!! and not developed!","how are you?","lol :D","am i joke to you?","-_-","you can lol"]
    if message.content == "hello":
        await message.channel.send(sample_texts[0])
    elif message.content == "you are dumb" or message.content == "you suck":
        await message.channel.send(sample_texts[2])
    elif message.content == "nice" or message.content =="noice":
        await message.channel.send(sample_texts[1])
    elif message.content == "no" or message.content == "nah":
        await message.channel.send("https://cdn.discordapp.com/emojis/790122638470676510.png?v=1")
    elif message.content == "ok" or message.content == "okay":
        await message.channel.send("https://cdn.discordapp.com/emojis/790123077396594688.png?v=1")
    responses = random.choice(sample_texts)
    if message.content == "lol" or message.content == "lmao":
        await message.channel.send(responses)
    
    for word in filtered_words:
        if word in message.content  :
            await message.delete()
            await message.channel.send(f"Stop using that word again {message.author.mention}")
            
    try:
        if message.mentions[0] == bot.user:

            with open("prefixes.json", "r") as f:
                prefixes = json.load(f)

            pre = prefixes[str(message.guild.id)] 

            await message.channel.send(f"My prefix for this server is {pre}")

    except:
        pass
    
    await bot.process_commands(message)
        
    
#############################################################################################################    
    
    
# @bot.event 
# async  def on_error(event , *args , **kwargs):
#     with open("err.log" , 'a') as f:
#         if event == "on_message":
#             f.write(f"Unhandled message: {args[0]}\n")
#         else:
#             raise 
  
#############################################################################################################  
    
@bot.command(name = "roll",help = "rolls dice")
async def roll(ctx, number_of_dice : int,number_of_sides:int):
    dice = [str(random.choice(range(1,number_of_sides+1))) 
            for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

#############################################################################################################
        
@bot.command()
async def deletechannel(ctx,channel:discord.TextChannel):
    embed = discord.Embed(
        title = "Success",
        description = f"Channel:{channel} has been deleted"
    )
    if ctx.author.guild_permissions.manage_channels == True:
        await ctx.send(embed = embed)
        await channel.delete()
    else:
        await ctx.send("you cannot delete a channel get perms noob!")

#############################################################################################################
        
@bot.command()
async def createchannel(ctx , channel):
    guild = ctx.guild
    embed = discord.Embed(
        title = "Success",
        description = f"Channel:{channel} has been created"
    )
    if ctx.author.guild_permissions.manage_channels == True:
        await guild.create_text_channel(name ='{}'.format(channel))
        await ctx.send(embed=embed)
    else:
        await ctx.send("you cannot create a channel get perms noob!")

#############################################################################################################

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx,member: discord.Member ,*,reason = " No reason Provided just banned lol"):
    await ctx.send(member.name + f" has been banned for: `{reason}`")
    await member.create_dm()
    await member.dm_channel.send(f"You have been banned for `{reason}`")
    await member.ban(reason = reason)
        
#############################################################################################################
    
@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, * , member):
    banned_users = await ctx.guild.bans()
    member_name,member_disc = member.split("#")
    for banned_entry in banned_users:
        user = banned_entry.user
        if(user.name,user.discriminator) == (member_name,member_disc):
            await ctx.guild.unban(user)
            await ctx.send(member_name + " has been unbanned XD!")
            return
    await ctx.send(member+ " was not found! **disappeared??**")
    

#############################################################################################################

# @bot.event
# async  def on_command_error(ctx,error):
#     try:
#         if isinstance(error,commands.errors.CheckFailure):
#                 await ctx.send("You dont have permission to do that! XD")
#         elif isinstance(error , commands.CommandNotFound):
#             await ctx.send("This command do not exist use `noah help` to see the commands available")
#     except discord.errors.Forbidden:
#         await ctx.send("Make sure I have the following permissions: `Manage Messages`, `Read Message History`, "
#                        "`Add Reactions`, `Mute Members`")


#############################################################################################################        
    
@bot.command()
async def wanted(ctx,user:discord.Member = None):
    if user == None:
        user = ctx.author
        await ctx.send("you didnt mention anyone, so you are the one who is wanted now!! XD")
    wanted = Image.open("Images/wanted.jpg")
    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    profile = Image.open(data)
    profile = profile.resize((244,242))
    wanted.paste(profile,(76,193))
    wanted.save("profile.jpg")
    
    await ctx.send(file = discord.File("profile.jpg"))

#############################################################################################################
    
@bot.command()
async def slap(ctx,user:discord.Member = None):
    if user == None:
        await ctx.send("Mention anyone to slap")
    else:
        slap = Image.open("Images/slap.jpg")
        
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
        
#############################################################################################################

@bot.command()
async def dead(ctx,user:discord.Member = None):
    if user == None:
        await ctx.send("Mention anyone to slap")
    else:
        slap = Image.open("Images/deadlol.jpg")
        
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

#############################################################################################################
        
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
  await member.kick(reason=reason)
    

    
    

    
    
bot.run(TOKEN)