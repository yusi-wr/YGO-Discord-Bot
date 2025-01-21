from nextcord import slash_command, Interaction, SlashOption, TextChannel, Member, User
from nextcord.ext import commands
from core import CommandTourna, Functions
from config import config

class Tournaments(commands.Cog):
	"""Tournaments commands"""
	COG_EMOJI = config["emoji"]["cmd"]["tournaments"]
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.commands = CommandTourna(self.bot)
		self.functions = Functions(self.bot)
		
	
	# a ctx command
	@commands.command(name="t-start")
	@commands.guild_only()
	async def StartRounds(self, ctx: commands.Context):
		"""Command start rounds of tournaments"""
		
		if self.functions.CheckPermisions(user=ctx.author):
			await self.commands.StartRound(ctx)
		else:
			await self.functions.NonHasPermisions(ctx=ctx)
	
	# a ctx command
	@commands.command(name="t-remove")
	@commands.guild_only()
	async def RomveUser(self, ctx: commands.Context, user: User):
		"""command for remove player from participants"""
		
		if self.functions.CheckPermisions(user=ctx.author):
			await self.commands.RomverUser(ctx, user)
		else:
			await self.functions.NonHasPermisions(ctx=ctx)
	
	#a ctx command
	@commands.command(name="t-qualify")
	@commands.guild_only()
	async def QualifyPlayer(self, ctx: commands.Context, user: User):
		"""command for qualify players"""
		
		if self.functions.CheckPermisions(user=ctx.author):
			await self.commands.QualifyPlayer(ctx, user)
		else:
			await self.functions.NonHasPermisions(ctx=ctx)
	
	#a ctx command
	@commands.command(name="t-exclude")
	@commands.guild_only()
	async def ExcludePlayer(self, ctx: commands.Context, user: User):
		"""command for exclude players"""
		
		if self.functions.CheckPermisions(user=ctx.author):
			await self.commands.ExcludePlayer(ctx, user)
		else:
			await self.functions.NonHasPermisions(ctx=ctx)
	
	# a command for confirm match of players
	@commands.command(name="t-match")
	@commands.guild_only()
	async def MatchConfirm(self, ctx: commands.Context, winner: User, loser: User, log_score):
		
		if self.functions.CheckPermisions(user=ctx.author):
			await self.commands.MatchConfirm(ctx=ctx, winner=winner, loser=loser, match_sorce=log_score)
		else:
			await self.functions.NonHasPermisions(ctx=ctx)
			
	# a ctx command
	@commands.command(name="t-delete")
	@commands.guild_only()
	async def DeleteTourna(self, ctx: commands.Context, *,reason=None):
		"""Command delete your tournament"""
		
		if self.functions.CheckPermisions(user=ctx.author):
			await self.commands.DeleteTournament(ctx=ctx, reason=reason)
		else:
			await self.functions.NonHasPermisions(ctx=ctx)
	
	# a ctx command
	@commands.command(name="t-end")
	@commands.guild_only()
	async def EndTourna(self, ctx: commands.Context, winner: User, winner2: User, winner3: User=None):
		"""command for ending a tournaments"""
		
		if self.functions.CheckPermisions(user=ctx.author):
			await self.commands.EndTournament(ctx=ctx, winner=winner, winner2=winner2, winner3=winner3)
		else:
			await self.functions.NonHasPermisions(ctx=ctx)
	
	
	# a slash command
	@slash_command(name="create-touranment", description="create tournaments")
	@commands.guild_only()
	async def CreateTourna(self, interaction: Interaction,
	   name: str = SlashOption(name="title", description="Name of the tournament"),
	   desc: str = SlashOption(name="description", description="You information or desc"),
	   channel_announce: TextChannel = SlashOption(name="announce-in", description="announce channel"),
	   log_channel: TextChannel = SlashOption(name="log-channel", description="log channel or your one for score`s"),
	   
	   ):
	   	"""slash command create tournaments"""
	   	
	   	if self.functions.CheckPermisions(interaction.user):
	   		await self.commands.CreateTourna(interaction=interaction, name=name, desc=desc, announc_channel=channel_announce,log_channel=log_channel)
	   	else:
	   		await self.functions.NonHasPermisions(interaction=interaction)
	
	
	
	
	
	
	
	
	
def setup(bot):
	bot.add_cog(Tournaments(bot))