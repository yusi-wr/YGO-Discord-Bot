from nextcord.ui import Select, View, button, Button, Modal, TextInput
from nextcord import Embed, Interaction, SelectOption, ButtonStyle, Message, User
from .data import cards_data
from .cards import Card
from config import config

emote = config["emoji"]

#Select menu for serach by list 
class SelectSearch(Select):
	def __init__(self, names):
		super().__init__(placeholder="Select cards...", max_values=1,options=[SelectOption(label=name, description="Select to retrieve card information", emoji=emote["list"]) for name in names])
		self.names = names
		
	async def callback(self, interaction: Interaction):
		
		if self.values:
			card = Card(cards_data[self.values[0]])
			await interaction.message.edit(embed=await card.embed_cards())
	

class PagesCards(View):
	def __init__(self, msg: Message, embeds: list, auther: User, names):
		super().__init__(timeout=180)
		
		self.page = 1
		self.names = names
		self.msg = msg
		self.author = auther
		self.embeds = embeds
		if len(self.names) <= 25:
			self.add_item(SelectSearch(names=self.names))
		
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
		page = Embed(title=f"**📑 Page: {self.page}/{len(self.embeds)}**")
		
		await interaction.message.edit(embeds=[embed, page])
	
	#back home button
	@button(style=ButtonStyle.red, emoji=emote["home"])
	async def Home(self, button: Button, interaction: Interaction):
		
		user = interaction.user
		if user.id != self.author.id:
			await interaction.response.send_message(f"**Sorry only {self.author.mention} can use this button**", ephemeral=True)
			return
		
		self.page = 1
			
		embed: Embed = self.embeds[self.page - 1]
		
		page = Embed(title=f"**📑 Page: {self.page}/{len(self.embeds)}**")
		
		await interaction.message.edit(embeds=[embed, page])
	
	
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
		page = Embed(title=f"**📑 Page: {self.page}/{len(self.embeds)}**")
		
		await interaction.message.edit(embeds=[embed, page])
		

#view for use it in command art/images
class View_Arts_Images(View):
	def __init__(self, embed, images, msg):
		super().__init__()
		
		self.page = 1
		self.message = msg
		self.embed: Embed = embed 
		self.images = images
		
	async def on_timeout(self):
		for button in self.children:
			button.disabled = True
			
		await self.message.edit(view=self)
		
	#button backward
	@button(style=ButtonStyle.gray, emoji=emote["back"])
	async def Backword(self, button: Button, interaction: Interaction):
		
		self.page -= 1
		if self.page < 1:
			self.page = len(self.images)
		
		self.embed.set_image(url=self.images[self.page - 1])
		
		await interaction.response.defer()
		await interaction.message.edit(embed=self.embed)
	
	
	#button return home or main
	@button(style=ButtonStyle.red, emoji=emote["home"])
	async def Home(self, button: Button, interaction: Interaction):
		
		self.page = 1
		self.embed.set_image(url=self.images[self.page - 1])
		
		await interaction.response.defer()
		await interaction.message.edit(embed=self.embed)
	
	#button farward
	@button(style=ButtonStyle.gray, emoji=emote["ward"])
	async def Forward(self, button: Button, interaction: Interaction):
		
		self.page += 1
		if self.page > len(self.images):
			self.page = 1
		
		self.embed.set_image(url=self.images[self.page - 1])
		
		await interaction.response.defer()
		await interaction.message.edit(embed=self.embed)
		


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
		pages = Embed(title=f"**📑 Page: {page}/{len(self.embeds)}**")
		
		await interaction.message.edit(embeds=[embed, pages])
		