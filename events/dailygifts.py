from nextcord.ext import commands, tasks
from core import DailyGifts, Functions
from config import config
import asyncio

emote = config["emoji"]

class DailyGIFTS(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.functions = Functions(self.bot)
		self.is_started = False
	
	@tasks.loop(hours=24)
	async def DailyGift(self):
		embed = self.functions.embed(
			desc=f"Hello all brave players. The daily gift box is open and ready to deliver your gift. Be one of the lucky ones and get approximately 👇\n- Gems: {emote['gems']} 6,500\n- Points: {emote['points']} 50\n- Good luck 🐞",
			icon="https://cdn.discordapp.com/emojis/1258396254388621323.png"
		)
		channel = await self.bot.fetch_channel(1295015793754505226)
		
		msg = await channel.send("@everyone", embed=embed)
		await msg.edit(view=DailyGifts(bot=self.bot, msg=msg))
		
		
	@commands.Cog.listener()
	async def on_ready(self):
		"""for run"""
		if not self.is_started:
			self.DailyGift.start()
			self.is_started = True
			await asyncio.sleep(2)
			
		
	
		
def setup(bot):
	bot.add_cog(DailyGIFTS(bot))