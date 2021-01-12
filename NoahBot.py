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
import apraw



def get_prefix(client,message):
    
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix = get_prefix,intents = intents)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')


bot.remove_command("help") 


os.chdir("C:\\Users\\anisr\\OneDrive\\Desktop\\NoahBot\\")

@bot.command()
async def load(ctx,extension):
    bot.load_extension(f'Cogs.{extension}')
    ctx.channel.send("Cogs loaded")
    
@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(f'Cogs.{extension}')
    ctx.channel.send("Cogs unloaded")

for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"Cogs.{filename[:-3]}")

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
    await ctx.guild.me.edit(nick=f'[{prefix}] Noahbot')


#############################################################################################################        

@bot.command()
@commands.has_permissions(manage_channels =True)
async def purge(ctx,amount = 5):
    await ctx.channel.purge(limit = amount)
    
filtered_words = ['fuck','FUCK','fck','sex','pussy','mf','motherfucker','bitch','ass','ASS','thefuck','wtf','WTF']
    
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
@bot.command()
async def mute(ctx, member: discord.Member):
  guild = ctx.guild
  if discord.utils.get(ctx.guild.roles,name = "Muted"):
    await ctx.send("Mute role already exists!")
    var = discord.utils.get(ctx.guild.roles,name = "Muted")
    for channel in guild.channels:
        await channel.set_permissions(var, speak=False, send_messages=False)
        await member.add_roles(var)
  else:
    await guild.create_role(name = "Muted",color = discord.Color(0x0062ff))
    var = discord.utils.get(ctx.guild.roles,name = "Muted")
    for channel in guild.channels:
        await channel.set_permissions(var, speak=False, send_messages=False)
        await ctx.send("Muted role created!")
    await member.add_roles(var)
    

 
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
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
  await member.kick(reason=reason)
    
@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member : discord.Member, *, reason='placeholder'):
    await ctx.send(member.mention + ' has been warned for the reason of ' + reason)
    await member.send('You were warned in {} with the reason of {}'.format(ctx.guild.name, reason))
    
  


    
    
bot.run(TOKEN)