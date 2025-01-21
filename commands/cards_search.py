from nextcord.ext import commands
from nextcord import Interaction, slash_command, SlashOption
from config import config
from core import YGOFunctions, cards_name, archetype

class Yugioh(commands.Cog, name="Yu-Gi-Oh"):
	"""Search cards commands"""
	COG_EMOJI = config["emoji"]["cmd"]["ygo"]
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.ygo_search = YGOFunctions(self.bot)
	
	
	#a slash command
	@slash_command(name="card")
	async def GetCard(self, interaction: Interaction,name: str = SlashOption(name="name", description="the name of card")):
		"""Search card by name"""
		await self.ygo_search.SearchCards(interaction=interaction, name=name)
	
	
	#a slash command
	@slash_command(name="card-random")
	async def GetRandomCard(self, interaction: Interaction):
		"""Get a card by random"""
		await self.ygo_search.RandomSearch(interaction=interaction)
	
	#a slash command
	@slash_command(name="art-card")
	async def GetArtCard(self, interaction: Interaction,name: str = SlashOption(name="name", description="the name of card")):
		"""Get arts card by name"""
		await self.ygo_search.GetArtCards(interaction=interaction, name=name)
	
	
	#a slash command
	@slash_command(name="art-random")
	async def GetRandomArt(self, interaction: Interaction, hide_name = SlashOption(name="hide-name", description="hide the card name", required=False, choices=["yes", "no"])):
		"""Get art`s card by random"""
		await self.ygo_search.RandomArtCards(interaction=interaction, hide_name=hide_name)
	
	
	#a slash command
	@slash_command(name="card-image")
	async def GetImageCard(self, interaction: Interaction,name: str = SlashOption(name="name", description="the name of card")):
		"""Get images card by name"""
		await self.ygo_search.GetImageCards(interaction=interaction, name=name)
	
	
	#a slash command
	@slash_command(name="archetype")
	async def GetCardByArchetype(self, interaction: Interaction,name: str = SlashOption(name="name", description="the name of archetype")):
		"""Search cards by archetype"""
		await self.ygo_search.ArchetypeSearch(interaction=interaction, name=name)
	
	
	
	
	
	
	
	#-------------(autocomplete)
	
	#for archetype search
	@GetCardByArchetype.on_autocomplete("name")
	async def archetype_autocomplete(self, interaction, name: str):
	       
	       name = await self.ygo_search.clean(name)
	       await interaction.response.send_autocomplete([i for i in archetype if i.startswith(name)]) if name else []
	
	#for normal search
	@GetCard.on_autocomplete("name")
	@GetArtCard.on_autocomplete("name")
	@GetImageCard.on_autocomplete("name")
	async def searchautocomplete(self, interaction, name: str):
	       
	       name = await self.ygo_search.clean(name)
	       await interaction.response.send_autocomplete([i for i in cards_name if i.startswith(name)]) if name else []
		
		
def setup(bot):
	bot.add_cog(Yugioh(bot))