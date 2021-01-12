import datetime
import asyncio
import discord
from discord.ext import commands
import sqlite3

class level(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.Cog.listener()
	async def on_ready(self):
		print("level cog loaded")  