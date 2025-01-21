from  nextcord import User
from nextcord.ext import commands
from config import config
from core import Functions, CommandDuelSystem

context = commands.Context

class DuelsSystem(commands.Cog, name="Duels"):
	"""Duel commands"""
	COG_EMOJI = config["emoji"]["cmd"]["ygo"]
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.commands = CommandDuelSystem(self.bot)
		self.functions = Functions(self.bot)
	
	#a ctx command
	@commands.command(name="challenge")
	@commands.guild_only()
	async def Challenges(self, ctx: context, opponent: User, points=10):
		"""Create a challenge against a specific opponent You can only create one challenge"""
		await self.commands.Challenge(ctx=ctx, opponent=opponent, points=points)
		
	#a ctx command
	@commands.command(name="remove-lose", aliases=["r-lose"])
	@commands.guild_only()
	async def RemoveLose(self, ctx: context):
		"""Remove one lose number from your profile"""
		await self.commands.RemoveLose(ctx=ctx)
		
	#a ctx command
	@commands.command(name="show-challenge")
	@commands.guild_only()
	async def ShowChallenges(self, ctx: context, player: User=None):
		"""Show challenge by player or all"""
		await self.commands.ShowChallenges(ctx=ctx, player=player)
		
	#a ctx command
	@commands.command(name="accept-challenge", aliases=["a-challenge"])
	@commands.guild_only()
	async def AcceptChallenges(self, ctx: context, winner: User ,loser: User, score):
		"""Confirm challenge duels"""
		
		if self.functions.CheckPermisions(user=ctx.author):
			await self.commands.AcceptChallenge(ctx=ctx, winner=winner, loser=loser, score=score)
		else:
			await self.functions.NonHasPermisions(ctx=ctx)
	
	#a ctx command
	@commands.command(name="delete-challenge", aliases=["d-challenge"])
	@commands.guild_only()
	async def DeleteChallenges(self, ctx: context, player: User=None):
		"""Delete challenge duels"""
		
		await self.commands.DeleteChallenge(ctx=ctx, player=player)
	
	#a ctx command
	@commands.command(name="duel", aliases=["a-duel"])
	@commands.guild_only()
	async def AcceptNormalDuel(self, ctx: context, winner: User ,loser: User, score):
		"""Confirm normal duels"""
		
		if self.functions.CheckPermisions(user=ctx.author):
			await self.commands.NormalDuel(ctx=ctx, winner=winner, loser=loser, score=score)
		else:
			await self.functions.NonHasPermisions(ctx=ctx)
		
	#a ctx command
	@commands.command(name="duel-history")
	@commands.guild_only()
	async def HistoryDuel(self, ctx: context, player: User=None):
		"""Show duel history"""
		await self.commands.DuelsHistory(ctx=ctx, player=player)
		
	#a ctx command
	@commands.command(name="delete-history")
	@commands.guild_only()
	async def DeleteDuelHistory(self, ctx: context, *,date):
		"""Delete duel history by date"""
		
		await self.commands.DeleteHistory(ctx=ctx, date=date)
		


def setup(bot):
	bot.add_cog(DuelsSystem(bot))