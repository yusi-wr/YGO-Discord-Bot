from nextcord import Message
from nextcord.ext import commands, tasks
from colorama import Fore, Style
from core import ViewUpdates, Functions, YGOFunctions
import nextcord
from config import config
import asyncio
from random import choice

games = [
	"EDOPro™",
	"Dueling Nexus™",
	"Dueling book™"
]

class Events(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.ViewUpdate = ViewUpdates(self.bot)
		self.functions = Functions(self.bot)
		self.ygo_search = YGOFunctions(self.bot)
		
		self.started = False

	#----------------(tasks)
		
	@tasks.loop(minutes=15)
	async def Status(self):
		await  self.bot.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Developed by: @yusi_wr"))
		await asyncio.sleep(180)
		await self.bot.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.playing, name=choice(games)))
	
	#----------------(events)
	
	#@commands.Cog.listener()
#	async def on_member_join(self, member):
#		if member.bot:
#			return
#			
#		await self.functions.Welcome(user=member, guild=member.guild)
	
	#on_ready
	@commands.Cog.listener()
	async def on_ready(self):
		if not self.started:
			self.Status.start()
			self.started = True
			await asyncio.sleep(2)
			
		self.functions.Add_View()
		await self.ViewUpdate.Run()
		print(Fore.LIGHTMAGENTA_EX + " • Developed by: " + Fore.LIGHTRED_EX + "𝙔𝙐𝙎𝙄")
		print(Fore.LIGHTCYAN_EX + " • Name: " + Fore.LIGHTRED_EX + f"{self.bot.user.name}")
		print(Fore.LIGHTMAGENTA_EX + " • Bot is: " + Fore.LIGHTGREEN_EX + "Online")
	
		
def setup(bot):
	bot.add_cog(Events(bot))