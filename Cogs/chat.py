import discord
from discord.ext import commands
import wikipedia,os
from chatbot import Chat, register_call

class Chatbot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Chat bot loaded")
    @register_call("whoIs")
    def who_is(self,query,session_id = "general"):
        try:
            return wikipedia.summary(query)
        except Exception:
            for new_query in wikipedia.summary(new_query):
                try:
                    return wikipedia.summary(new_query)
                except Exception:
                    pass
        return f"I never heard of {query}"
        template_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"Chatbottemplate","chatbottemplate.template")
        chat = Chat(template_file_path)
    @commands.command()
    async def chat(self,ctx,*,message):
        template_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"Chatbottemplate","chatbottemplate.template")
        chat = Chat(template_file_path)
        result = chat.respond(message)
        if(len(result)<=2048):
            embed=discord.Embed(title="Noah Chat", description = result, color = (0xF48D1))
            await ctx.send(embed=embed)
        else:
            embedList = []
            n=2048
            embedList = [result[i:i+n] for i in range(0, len(result), n)]
            for num, item in enumerate(embedList, start = 1):
                if(num == 1):
                    embed = discord.Embed(title="ChatBot AI", description = item, color = (0xF48D1))
                    embed.set_footer(text="Page {}".format(num))
                    await ctx.send(embed = embed)
                else:
                    embed = discord.Embed(description = item, color = (0xF48D1))
                    embed.set_footer(text = "Page {}".format(num))
                    await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Chatbot(bot))
