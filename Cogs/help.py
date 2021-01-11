import discord
from discord.ext import commands
import DiscordUtils
import paginator

class help(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
    @commands.Cog.listener()    
    async def on_ready(self):
        print('help command loaded')
        
    
    @commands.command()
    async def help(self , ctx):
        embed1 = discord.Embed(color=ctx.author.color).add_field(name="**Moderations**",value = None)
        embed1.add_field(name = 'createchannel',value = 'creates a channel for you')
        embed1.add_field(name = 'deletechannel',value ='deletes a channel (give the name/id/mention the channel)')
        embed1.add_field(name = 'kick',value = 'kicks the member whom you mention')
        embed1.add_field(name = 'ban',value = 'bans the member whom you mention and wont allow him to join again unless unbanned')
        embed1.add_field(name = 'unban',value = 'unbans the member(give me the username with the code of the banned member)')
        embed1.add_field(name = 'mute',value = 'Mutes the person')
        embed1.add_field(name = 'unmute',value = 'coming soon!')
        embed1.add_field(name = 'warn',value = 'warns a person! in their dm')
        
        embed2 = discord.Embed(color=ctx.author.color).add_field(name="**Fun**",value = None)
        embed2.add_field(name = 'slap',value = 'mention a member to slap')
        embed2.add_field(name = 'dead',value = 'mention a member, and he is dead with your smile lol')
        embed2.add_field(name = 'wanted',value = 'mention a member whom you wanted to see him most wanted')
        embed2.add_field(name = 'roll',value='give me the sides and number of dices to use ;)')
        embed2.add_field(name = 'kill',value = 'mention a member and they are dead(dont formet to mention the reason too)')
        embed2.add_field(name = 'count',value = 'just count give me the limit too')
        embed2.add_field(name = 'allcommands',value = 'shows the number of commands!')
        
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
    
    
    
        
        
def setup(bot):
    bot.add_cog(help(bot))
    
        
        