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
import DiscordUtils
import praw

class Moderations(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
    @commands.Cog.listener()    
    async def on_ready(self):
        print('moderation command loaded')
    
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def changeprefix(self,ctx, prefix):

        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open("prefixes.json", "w") as f:
            json.dump(prefixes,f)    

        await ctx.send(f"The prefix was changed to {prefix}")
        await ctx.guild.me.edit(nick=f'[{prefix}] Noahbot')

    @commands.command()
    @commands.has_permissions(manage_channels =True)
    async def purge(self,ctx,amount = 5):
        await ctx.channel.purge(limit = amount)
    
    @commands.command()
    async def mute(self,ctx, member: discord.Member,time: int,d,*,reason = None):
        guild = ctx.guild
        if discord.utils.get(ctx.guild.roles,name = "Muted"):
            await ctx.send("Mute role already exists!")
            var = discord.utils.get(ctx.guild.roles,name = "Muted")
            for channel in guild.channels:
                await channel.set_permissions(var, speak=False, send_messages=False)
            await member.add_roles(var)
            embed = discord.Embed(title="muted!", description=f"{member.mention} has been muted ", colour=discord.Colour.light_gray())
            embed.add_field(name="reason:", value=reason, inline=False)
            embed.add_field(name="time left for the mute:", value=f"{time}{d}", inline=False)
            await ctx.send(embed=embed)
            if d == "s":
                await asyncio.sleep(time)

            if d == "m":
                await asyncio.sleep(time*60)

            if d == "h":
                await asyncio.sleep(time*60*60)

            if d == "d":
                await asyncio.sleep(time*60*60*24)

            await member.remove_roles(var)
            embed = discord.Embed(title="unmute (temp) ", description=f"unmuted -{member.mention} ", colour=discord.Colour.light_gray())
            await ctx.send(embed=embed)

        else:
            await guild.create_role(name = "Muted",color = discord.Color(0x0062ff))
            var = discord.utils.get(ctx.guild.roles,name = "Muted")
            for channel in guild.channels:
                await channel.set_permissions(var, speak=False, send_messages=False)
            await ctx.send("Muted role created!")
            await member.add_roles(var)
            embed = discord.Embed(title="muted!", description=f"{member.mention} has been tempmuted ", colour=discord.Colour.light_gray())
            embed.add_field(name="reason:", value=reason, inline=False)
            embed.add_field(name="time left for the mute:", value=f"{time}{d}", inline=False)
            await ctx.send(embed=embed)
            if d == "s":
                await asyncio.sleep(time)

            if d == "m":
                await asyncio.sleep(time*60)

            if d == "h":
                await asyncio.sleep(time*60*60)

            if d == "d":
                await asyncio.sleep(time*60*60*24)

            await member.remove_roles(var)
            embed = discord.Embed(title="unmute (temp) ", description=f"unmuted -{member.mention} ", colour=discord.Colour.light_gray())
            await ctx.send(embed=embed)

            

    @commands.command()
    async def deletechannel(self,ctx,channel:discord.TextChannel):
        embed = discord.Embed(
            title = "Success",
            description = f"Channel:{channel} has been deleted"
        )
        if ctx.author.guild_permissions.manage_channels == True:
            await ctx.send(embed = embed)
            await channel.delete()
        else:
            await ctx.send("you cannot delete a channel get perms noob!")
    
    @commands.command()
    async def createchannel(self,ctx , channel):
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
    
    @commands.command(name="ban")
    async def ban(self, context, member: discord.Member, *args):
        if context.message.author.guild_permissions.administrator:
            try:
                if member.guild_permissions.administrator:
                    embed = discord.Embed(
                        title="Error!",
                        description="User has Admin permissions.",
                        color=0x00FF00
                    )
                    await context.send(embed=embed)
                else:
                    reason = " ".join(args)
                    embed = discord.Embed(
                        title="User Banned!",
                        description=f"**{member}** was banned by **{context.message.author}**!",
                        color=0x00FF00
                    )
                    embed.add_field(
                        name="Reason:",
                        value=reason
                    )
                    await context.send(embed=embed)
                    await member.send(f"You were banned by **{context.message.author}**!\nReason: {reason}")
                    await member.ban(reason=reason)
            except:
                embed = discord.Embed(
                    title="Error!",
                    description="An error occurred while trying to ban the user.",
                    color=0x00FF00
                )
                await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0x00FF00
            )
            await context.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self,ctx, * , member):
        banned_users = await ctx.guild.bans()
        member_name,member_disc = member.split("#")
        for banned_entry in banned_users:
            user = banned_entry.user
            if(user.name,user.discriminator) == (member_name,member_disc):
                await ctx.guild.unban(user)
                await ctx.send(member_name + " has been unbanned XD!")
                return
        await ctx.send(member+ " was not found! **disappeared??**")
    
    @commands.command(name='kick', pass_context=True)
    async def kick(self, context, member: discord.Member, *args):
        if context.message.author.guild_permissions.kick_members:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    title="Error!",
                    description="User has Admin permissions.",
                    color=0x00FF00
                )
                await context.send(embed=embed)
            else:
                try:
                    reason = " ".join(args)
                    embed = discord.Embed(
                        title="User Kicked!",
                        description=f"**{member}** was kicked by **{context.message.author}**!",
                        color=0x00FF00
                    )
                    embed.add_field(
                        name="Reason:",
                        value=reason
                    )
                    await context.send(embed=embed)
                    try:
                        await member.send(
                            f"You were kicked by **{context.message.author}**!\nReason: {reason}"
                        )
                    except:
                        pass
                except:
                    embed = discord.Embed(
                        title="Error!",
                        description="An error occurred while trying to kick the user.",
                        color=0x00FF00
                    )
                    await context.message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0x00FF00
            )
            await context.send(embed=embed)
    
    @commands.command(name="warn")
    async def warn(self, context, member: discord.Member, *args):
        if context.message.author.guild_permissions.administrator:
            reason = " ".join(args)
            embed = discord.Embed(
                title="User Warned!",
                description=f"**{member}** was warned by **{context.message.author}**!",
                color=0x00FF00
            )
            embed.add_field(
                name="Reason:",
                value=reason
            )
            await context.send(embed=embed)
            try:
                await member.send(f"You were warned by **{context.message.author}**!\nReason: {reason}")
            except:
                pass
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0x00FF00
            )
            await context.send(embed=embed)
    @commands.command(name="poll")
    async def poll(self, context, *args):
        poll_title = " ".join(args)
        embed = discord.Embed(
            title="A new poll has been created!",
            description=f"{poll_title}",
            color=0x00FF00
        )
        embed.set_footer(
            text=f"Poll created by: {context.message.author} • React to vote!"
        )
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")
    
    @commands.has_permissions(manage_channels = True)
    @commands.command(name = "createvoice")
    async def createvoice(self,ctx,name,*,bitrate:int = None,user_limit:int = None):
        if bitrate == None:
            await ctx.send("Please give bitrate (recommended : 64)")
            if user_limit == None:
                await ctx.send("Please give user limit")
            else:
                return
        else:
            await ctx.guild.create_voice_channel(name = name,bitrate = bitrate*1000,user_limit=user_limit)

    @commands.has_permissions(manage_guild = True)
    @commands.command(name = "editserver")
    async def editserver(self,ctx,name:str=None,description:str = None,icon:bytes =None,banner:bytes=None,owner=discord.Member):
        try:
            await ctx.guild.edit(name = name,description = description,icon = icon,banner=banner,owner=owner)
        except discord.Forbidden:
            await ctx.send("you dont have permissions to do that noob!")
        except discord.HTTPException:
            await ctx.send("failed editing the server")
        except discord.InvalidArgument:
            await ctx.send("something went wrong!")



    @commands.has_permissions(manage_guild = True)
    @commands.command(name = "makerole")
    async def createrole(self,ctx,name,color):
        dictOfColors = { 'default' : discord.Color.default(),
                        'teal' : discord.Color.teal(),
                        'darkteal' : discord.Color.dark_teal(),
                        'green' : discord.Color.green(),
                        'darkgreen' : discord.Color.dark_green(),
                        'blue' : discord.Color.blue(),
                        'purple' : discord.Color.purple(),
                        'darkpurple' : discord.Color.dark_purple(),
                        'magenta' : discord.Color.magenta(),
                        'darkmagenta' : discord.Color.dark_magenta(),
                        'gold' : discord.Color.gold(),
                        'darkgold' : discord.Color.dark_gold(),
                        'orange' : discord.Color.orange(),
                        'darkorange' : discord.Color.dark_orange(),
                        'red' : discord.Color.red(),
                        'darkred' : discord.Color.dark_red() }
        guild = ctx.guild
        await guild.create_role(name = name,color = dictOfColors[color])
        await ctx.send(f"Role `{name}` has been created!")




    @commands.has_permissions(manage_guild = True)
    @commands.command()
    async def giverole(self,ctx, member: discord.Member,name: str,color):
        dictOfColors = { 'default' : discord.Color.default(),
                        'teal' : discord.Color.teal(),
                        'darkteal' : discord.Color.dark_teal(),
                        'green' : discord.Color.green(),
                        'darkgreen' : discord.Color.dark_green(),
                        'blue' : discord.Color.blue(),
                        'purple' : discord.Color.purple(),
                        'darkpurple' : discord.Color.dark_purple(),
                        'magenta' : discord.Color.magenta(),
                        'darkmagenta' : discord.Color.dark_magenta(),
                        'gold' : discord.Color.gold(),
                        'darkgold' : discord.Color.dark_gold(),
                        'orange' : discord.Color.orange(),
                        'darkorange' : discord.Color.dark_orange(),
                        'red' : discord.Color.red(),
                        'darkred' : discord.Color.dark_red() }
        guild = ctx.guild
        if discord.utils.get(ctx.guild.roles,name = name):
            await ctx.send(f"`{name}` role already exists!")
            var = discord.utils.get(ctx.guild.roles,name = name)
            for channel in guild.channels:
                await channel.set_permissions(var, speak=True, send_messages=True)
            await member.add_roles(var)
            await ctx.send(f"{name} role given to {member.mention}")
        else:
            await guild.create_role(name = name,color = dictOfColors[color])
            var = discord.utils.get(ctx.guild.roles,name = name)
            for channel in guild.channels:
                await channel.set_permissions(var, speak=True, send_messages=True)
            await ctx.send(f"`{name}` role created!")
            await member.add_roles(var)
            await ctx.send(f"{name} role given to {member.mention}")
        



def setup(bot):
    bot.add_cog(Moderations(bot))