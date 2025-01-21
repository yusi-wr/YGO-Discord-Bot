from nextcord import User
from nextcord.ext import commands
from core import Functions, MyHelpCommand, CommandPointsSystem
from config import config
import datetime

context = commands.Context

class General(commands.Cog, name="General"):
	"""General commands"""
	COG_EMOJI = config["emoji"]["cmd"]["general"]
	def __init__(self, bot):
	      self._original_help_command = bot.help_command
	      bot.help_command = MyHelpCommand()
	      bot.help_command.cog = self
	      self.bot = bot
	      self.commands = CommandPointsSystem(self.bot)
	      self.function = Functions(self.bot)
	      self.start_time = datetime.datetime.utcnow()
	
	def cog_unload(self):
		self.bot.help_command = self._original_help_command
	
	#a context command
	@commands.command(name="profile", aliases=["pro", "user"])
	@commands.guild_only()
	async def ShowProfile(self, ctx: context, user: User=None):
		"""Show user`s profile ^_^"""
		
		await self.commands.ProfileUser(ctx=ctx, user=user)
	
	#a context command
	@commands.command(name="transfer", aliases=["tr", "to"])
	@commands.guild_only()
	async def TransferGems(self, ctx: context, user: User, gem: int):
		"""Transfer gems to other user`s"""
		await self.commands.Transfer(ctx=ctx, user=user, gem=gem)
		
	#a context command
	@commands.command(name="daily", aliases=["dy"])
	@commands.guild_only()
	async def Daily(self, ctx: context):
		"""Transfer gems to other user`s"""
		
		await self.commands.Daily(ctx=ctx)
	
	#a context command
	@commands.command(name="buy-points", aliases=["buy", "shop", "points"])
	@commands.guild_only()
	async def BuyPoints(self, ctx: context, points: str = None):
		"""Buy points"""
		
		await self.commands.BuyPoints(ctx=ctx, points=points)
		
	# a context command
	@commands.command(name="uptime", aliases=["up"])
	async def Uptime(self, ctx: context):
		"""Show uptime bot"""
		await self.commands.Uptime(ctx=ctx, start_time=self.start_time)
		
	# a context command
	@commands.command(name="ping")
	async def Ping(self, ctx: context):
		"""Show latency bot"""
		await self.commands.ping(ctx=ctx)
	
	
	
	
	
def setup(bot: commands.Bot):
    bot.add_cog(General(bot))