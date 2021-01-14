import random
import discord
import urllib
import secrets
import asyncio
import aiohttp
import re
import http
import requests
import datetime
from io import BytesIO
from discord.ext import commands
import utils

class Fun_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def f(self, ctx, *, text: commands.clean_content = None):
        hearts = ['❤', '💛', '💚', '💙', '💜']
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")   
    
    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def urban(self, ctx, *, search: commands.clean_content):  
        async with ctx.channel.typing():
            try:
                url = await http.get(f'https://api.urbandictionary.com/v0/define?term={search}', res_method="json")
            except Exception:
                return await ctx.send("Urban API returned invalid data... might be down atm.")

            if not url:
                return await ctx.send("I think the API broke...")

            if not len(url['list']):
                return await ctx.send("Couldn't find your search in the dictionary...")

            result = sorted(url['list'], reverse=True, key=lambda g: int(g["thumbs_up"]))[0]

            definition = result['definition']
            if len(definition) >= 1000:
                definition = definition[:1000]
                definition = definition.rsplit(' ', 1)[0]
                definition += '...'

            await ctx.send(f"📚 Definitions for **{result['word']}**```fix\n{definition}```")
    @commands.command(helpinfo='Searches the web (or images if typed first)', aliases=['search'])
    async def google(self,ctx, *, searchquery: str):
        '''
        Should be a group in the future
        Googles searchquery, or images if you specified that
        '''
        searchquerylower = searchquery.lower()
        if searchquerylower.startswith('images '):
            await ctx.send('<https://www.google.com/search?tbm=isch&q={}>'
                        .format(urllib.parse.quote_plus(searchquery[7:])))
        else:
            await ctx.send('<https://www.google.com/search?q={}>'
                        .format(urllib.parse.quote_plus(searchquery)))

    @commands.command(helpinfo='Wikipedia summary', aliases=['w', 'wiki'])
    async def wikipedia(self,ctx, *, query: str):
        '''
        Uses Wikipedia APIs to summarise search
        '''
        sea = requests.get(
            ('https://en.wikipedia.org//w/api.php?action=query'
            '&format=json&list=search&utf8=1&srsearch={}&srlimit=5&srprop='
            ).format(query)).json()['query']

        if sea['searchinfo']['totalhits'] == 0:
            await ctx.send('Sorry, your search could not be found.')
        else:
            for x in range(len(sea['search'])):
                article = sea['search'][x]['title']
                req = requests.get('https://en.wikipedia.org//w/api.php?action=query'
                                '&utf8=1&redirects&format=json&prop=info|images'
                                '&inprop=url&titles={}'.format(article)).json()['query']['pages']
                if str(list(req)[0]) != "-1":
                    break
            else:
                await ctx.send('Sorry, your search could not be found.')
                return
            article = req[list(req)[0]]['title']
            arturl = req[list(req)[0]]['fullurl']
            artdesc = requests.get('https://en.wikipedia.org/api/rest_v1/page/summary/'+article).json()['extract']
            lastedited = datetime.datetime.strptime(req[list(req)[0]]['touched'], "%Y-%m-%dT%H:%M:%SZ")
            embed = discord.Embed(title='**'+article+'**', url=arturl, description=artdesc, color=0x3FCAFF)
            embed.set_footer(text='Wiki entry last modified',
                            icon_url='https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png')
            embed.set_author(name='Wikipedia', url='https://en.wikipedia.org/',
                            icon_url='https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png')
            embed.timestamp = lastedited
            await ctx.send('**Search result for:** ***"{}"***:'.format(query), embed=embed)



def setup(bot):
    bot.add_cog(Fun_Commands(bot))
 
    
