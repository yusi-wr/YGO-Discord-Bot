from nextcord import Embed, User, Interaction, Member, ButtonStyle
from nextcord.ui import Button, View, button
from config import config
from database import users, Load, Update

emote = config["emoji"]

class Verify(View):
	def __init__(self, user: Member, role):
		super().__init__(timeout=None)
		self.user = user
		self.role = role
	
	@button(label="Verify", style=ButtonStyle.grey, emoji=emote["verify"])
	async def Verify(self, button: Button, interaction: Interaction):
		
		if interaction.user.id != self.user.id:
			await interaction.response.send_message(embed=Embed(color=config["embed-color"], description=f"**Sorry, for {self.user.mention} only**"), ephemeral=True)
			return
		
		users.Load(self.user)
		data = Load("verifiy.json")
		data["users"].append(self.user.id)
		Update(file="verifiy.json", data=data)
		await self.user.add_roles(self.role)
		
		self.Verify.label = "Done"
		self.Verify.disabled=True
		await interaction.message.edit(view=self)
		
		await interaction.response.send_message(embed=Embed(description="**You have been verified**"), ephemeral=True)
		
		
	
	