from nextcord import User
from nextcord.ext import commands
from core import Functions, CommandPointsSystem
from config import config

context = commands.Context

class Admins(commands.Cog, name="Admins"):
	"""Admin commands"""
	COG_EMOJI = config["emoji"]["cmd"]["admin"]
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.commands_points = CommandPointsSystem(self.bot)
		self.functions = Functions(self.bot)
	
	
	#a ctx command
	@commands.command(name="a-DP", aliases=["dp"])
	@commands.guild_only()
	async def AddDP(self, ctx: context, user: User, dp: int):
		"""Add dp points to any user - min: 1/ max: 50"""
		
		if self.functions.CheckPermisions(user=ctx.author):
			await self.commands_points.AddDPToUser(ctx=ctx, user=user, DP=dp)
		else:
			await self.functions.NonHasPermisions(ctx=ctx)
	
	#a ctx command
	@commands.command(name="a-Gems", aliases=["gems", "g"])
	@commands.guild_only()
	async def AddGems(self, ctx: context, user: User, Gems: int):
		"""Add gems to any user - min: 1/ max: 25000"""
		
		if self.functions.CheckPermisions(user=ctx.author):
			await self.commands_points.AddGemsToUser(ctx=ctx, user=user, Gems=Gems)
		else:
			await self.functions.NonHasPermisions(ctx=ctx)
	
	
	


def setup(bot: commands.Bot):
    bot.add_cog(Admins(bot))