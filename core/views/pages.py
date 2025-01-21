from nextcord.ext import commands
from nextcord import Embed, Interaction, ButtonStyle, Message, User
from nextcord.ui import View, Button, button, Modal, TextInput
from config import config

emote = config["emoji"]
 
class Pages(View):
	def __init__(self, msg: Message, embeds: list, auther: User):
		super().__init__(timeout=180)
		
		self.msg = msg
		self.author = auther
		self.embeds = embeds
		self.page = 1
		
	async def on_timeout(self):
		for button in self.children:
			button.disabled=True
		
		await self.msg.edit(view=self)
	
	#backward button
	@button(style=ButtonStyle.gray, emoji=emote["back"])
	async def Backword(self, button: Button, interaction: Interaction):
		
		user = interaction.user
		if user.id != self.author.id:
			await interaction.response.send_message(f"**Sorry only {self.author.mention} can use this button**", ephemeral=True)
			return
			
		self.page -= 1
		if self.page < 1:
			self.page = len(self.embeds)
			
		embed: Embed = self.embeds[self.page - 1]
		embed.set_footer(text=f"📑 Page: {self.page}/{len(self.embeds)} | By: {self.author.name}")
		
		await interaction.message.edit(embed=embed)
	
	#back home button
	@button(style=ButtonStyle.red, emoji=emote["home"])
	async def Home(self, button: Button, interaction: Interaction):
		
		user = interaction.user
		if user.id != self.author.id:
			await interaction.response.send_message(f"**Sorry only {self.author.mention} can use this button**", ephemeral=True)
			return
		
		self.page = 1
			
		embed: Embed = self.embeds[self.page - 1]
		embed.set_footer(text=f"📑 Page: {self.page}/{len(self.embeds)} | By: {self.author.name}")
		
		await interaction.message.edit(embed=embed)
	
	
	#back home button
	@button(style=ButtonStyle.red, emoji=emote["list"])
	async def ToPage(self, button: Button, interaction: Interaction):
		
		user = interaction.user
		if user.id != self.author.id:
			await interaction.response.send_message(f"**Sorry only {self.author.mention} can use this button**", ephemeral=True)
			return
		
		
		await interaction.response.send_modal(ModelSelectPage(embeds=self.embeds))
	
	#Forward button
	@button(style=ButtonStyle.gray, emoji=emote["ward"])
	async def Forward(self, button: Button, interaction: Interaction):
		
		user = interaction.user
		if user.id != self.author.id:
			await interaction.response.send_message(f"**Sorry only {self.author.mention} can use this button**", ephemeral=True)
			return
			
		self.page += 1
		if self.page > len(self.embeds):
			self.page = 1
			
		embed: Embed = self.embeds[self.page - 1]
		embed.set_footer(text=f"📑 Page: {self.page}/{len(self.embeds)} | By: {self.author.name}")
		
		await interaction.message.edit(embed=embed)



class ModelSelectPage(Modal):
	def __init__(self, embeds):
		super().__init__(title="Select Page by Number", timeout=None)
		
		self.embeds = embeds
		
		self.page = TextInput(
		     label="Write the page number",
		     min_length=1,
		     max_length=2,
		     required=True,
		     placeholder="Move to the specified page"
		)
		self.add_item(self.page)
		
	async def callback(self, interaction: Interaction):
		
		if int(self.page.value) > len(self.embeds):
			await interaction.response.send_message(f"Sorry, you have entered a number higher than the number of pages. Please enter a valid number\nThe highest number of pages `{len(self.embeds)}`", ephemeral=True)
			return
			
		user = interaction.user
		page = int(self.page.value)
		embed: Embed = self.embeds[page - 1]
		embed.set_footer(text=f"📑 Page: {page}/{len(self.embeds)} | By: {user.name}")
		
		await interaction.message.edit(embed=embed)
		