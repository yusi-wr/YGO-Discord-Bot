from nextcord import Embed, User, Interaction, ButtonStyle
from nextcord.ui import View, Button, button
from database import challenges
from config import config
from .embeds import *

emote = config["emoji"]


#class view for challenges confirm
class ChallengeConfirm(View):
	def __init__(self, player: User, opponent: User, points, msg):
		super().__init__(timeout=180)
		
		self.msg = msg
		self.player = player
		self.opponent = opponent
		self.points = points
		
	async def on_timeout(self):
		for button in self.children:
			button.disabled=True
			
		await self.msg.edit(view=self)
	
	#button confirm
	@button(style=ButtonStyle.green, emoji=emote["yes"])
	async def Confirm(self, button: Button, interaction: Interaction):
		
		user = interaction.user
		
		if user.id == self.player.id:
			await interaction.response.send_message(f"**Please excuse the player's response {self.opponent.mention}**", ephemeral=True)
			return
		elif user.id != self.opponent.id:
			await interaction.response.send_message(f"**Sorry, this button is only for player {self.opponent.mention}**", ephemeral=True)
			return
			
		challenges.Create(player=self.player, opponent=self.opponent, points=self.points)
		
		await interaction.message.edit(embed=embed_challenge_start(player=self.player, opponent=self.opponent, points=self.points), view=None)
	
	#button cancel
	@button(style=ButtonStyle.red, emoji=emote["no"])
	async def Cencal(self, button: Button, interaction: Interaction):
		
		user = interaction.user
		
		if user.id == self.player.id:
			await interaction.response.send_message(f"**Please excuse the player's response {self.opponent.mention}**", ephemeral=True)
			return
		elif user.id != self.opponent.id:
			await interaction.response.send_message(f"**Sorry, this button is only for player {self.opponent.mention}**", ephemeral=True)
			return
			
		await interaction.message.edit(embed=embed_cancel_challenge(player=self.player, opponent=self.opponent, points=self.points))
		
		await self.on_timeout()
		