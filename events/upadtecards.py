from nextcord.ext import commands, tasks
import asyncio
from core import YGOFunctions
from config import config

class UpdateCards(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.ygo = YGOFunctions(self.bot)
		self.started = False
		
	@tasks.loop(hours=24)
	async def Updater(self):
		await self.ygo.update_cards()
		
	
	#on_ready
	@commands.Cog.listener()
	async def on_ready(self):
		if not self.started:
			self.Updater.start()
			self.started = True
			await asyncio.sleep(2)
		
		

def setup(bot):
	bot.add_cog(UpdateCards(bot))