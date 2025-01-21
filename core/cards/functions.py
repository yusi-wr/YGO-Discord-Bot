import requests
from urllib.parse import quote
from difflib import get_close_matches
from .data import cards_data, cards_id, api, cards_art, cards_images, cards_name, archetype
from nextcord import Interaction, Embed, Message
from nextcord.ext import commands
import asyncio
from colorama import Fore, Style
from string import punctuation
from .cards import Card
from .views import PagesCards, View_Arts_Images
from random import choice
import os
from core import Functions
from config import config
from database import Load

emote = config["emoji"]
loading = Embed(description=f"**{emote['loading']} Loading...**", color=config["embed-color"])

#calss functions help
class YGOFunctions:
	def __init__(self, bot: commands.Bot=None):
		self.bot = bot
		self.functions = Functions(self.bot)
	
	
	async def clean(self, text):
   	 '''Remove punctuation and unicode from the text, convert it to lowercase and return it'''
   	 return (
      	  ' '.join(text.translate(str.maketrans({mark : ' ' for mark in punctuation})).split())
           .encode('ascii', 'ignore')
           .decode()
           .lower()
           )
    
	async def fuzzy(self, comparate, comparables, results=25):
	    '''Compare the comparate with the comparables and return results'''
	    
	    return get_close_matches(comparate, comparables, cutoff=0.1, n=results)
	
	#-----------------------------------
	
	# function update cards data
	async def update_cards(self):
		
		data = requests.get(url=api, params={"misc":"yes"}).json()["data"]
		
		new_cards = []
		
		if data:
			copyname = cards_name.copy()
			cards_data.clear()
			cards_art.clear()
			cards_id.clear()
			cards_images.clear()
			cards_name.clear()
			archetype.clear()
			
			for card in data:
				name = await self.clean(card["name"])
				ID = card["id"]
				cards_data[name] = card
				cards_name.append(name)
				
				if "archetype" in card:
					Archetype = await self.clean(card["archetype"])
					if Archetype in archetype:
						archetype[Archetype].append(name)
					else:
						archetype[Archetype] = []
						archetype[Archetype].append(name)
				
				for images in card["card_images"]:
					cards_images[images["id"]] = {}
					cards_images[images["id"]]["name"] = name
					cards_images[images["id"]]["url"] = images["image_url"]
					cards_art[images["id"]] = {}
					cards_art[images["id"]]["name"] = name
					cards_art[images["id"]]["url"] = images["image_url_cropped"]
					cards_id[str(images["id"])] = name
					
				if name not in copyname:
					new_cards.append(name)
			
			
			print(Fore.LIGHTMAGENTA_EX + " • Update cards: " + Fore.LIGHTGREEN_EX + f"{len(cards_data)} "+ Style.RESET_ALL)
			
			if len(new_cards) >= 1:
				await self.NewCards(new_cards=new_cards)
				
	
	#function search command'
	async def SearchCards(self, interaction: Interaction, name):
		
		name = await self.clean(name)
		try:
			card = Card(card=cards_data[name])
			await interaction.response.send_message(embed=await card.embed_cards())
		except:
			await self.NoResult(interaction=interaction)
	
	#function for search cards list by archetype
	async def ArchetypeSearch(self, interaction: Interaction, name: str):
		
		guild = interaction.guild
		user = interaction.user
		
		msg = await interaction.response.send_message(embed=loading)
		
		name = await self.clean(name)
		list_name = sorted(archetype[name])
		
		if list_name:
			card = Card(card=cards_data[list_name[0]])
			if len(list_name) > 1:
				embeds = [await Card(card=cards_data[x]).embed_cards() for x in list_name]
				view=PagesCards(msg=msg, embeds=embeds, auther=user, names=list_name)
				await msg.edit(embed=await card.embed_cards(), view=view)
			else:
				await msg.edit(embed=await card.embed_cards())
		else:
			await msg.edit(embed=Embed(color=config["embed-color"], description=">>> **No results found, please try again**"))
	
	#search cards by random
	async def RandomSearch(self, interaction: Interaction):
		
		name = choice(cards_name)
		card = Card(cards_data[name])
		await interaction.response.send_message(embed=await card.embed_cards())
	
	#get cards arts
	async def GetArtCards(self, interaction: Interaction, name):
		
		name = await self.clean(name)
		try:
			card = Card(card=cards_data[name])
			embed = await card.embed_arts()
			
			msg = await interaction.response.send_message(embed=embed)
			
			images = [cards_art[i]["url"] for i in cards_art if cards_art[i]["name"] == name]
			
			if len(images) > 1:
				await msg.edit(view=View_Arts_Images(embed=embed, images=images, msg=msg))
		except:
			await self.NoResult(interaction=interaction)
	
	
	#get cards arts by random
	async def RandomArtCards(self, interaction: Interaction, hide_name="no"):
		
		guild = interaction.guild
		
		name = choice(cards_name)
		try:
			card = Card(card=cards_data[name])
			embed: Embed = await card.embed_arts()
			if hide_name == "yes":
				embed.set_author(name="hide name ✓", icon_url=embed.author.icon_url)
			
			msg = await interaction.response.send_message(embed=embed)
			
			images = [cards_art[i]["url"] for i in cards_art if cards_art[i]["name"] == name]
			
			if len(images) > 1:
				await msg.edit(view=View_Arts_Images(embed=embed, images=images, msg=msg))
		except:
			await self.NoResult(interaction=interaction)
	
	
	#(copy from function GetArtCards) but now get normal image
	async def GetImageCards(self, interaction: Interaction, name):
		
		name = await self.clean(name)
		try:
			card = Card(card=cards_data[name])
			embed = await card.embed_normal_images()
			
			msg = await interaction.response.send_message(embed=embed)
			
			images = [cards_images[i]["url"] for i in cards_images if cards_images[i]["name"] == name]
			
			if len(images) > 1:
				await msg.edit(view=View_Arts_Images(embed=embed, images=images, msg=msg))
		except:
			await self.NoResult(interaction=interaction)
	
	#search cards from user message <>
	async def EventSearch(self, message: Message):
		
		black_list = ["<@!", "<@&", "<:", "<:a", "<?", "<#", "<&", "<$", "<%", "<.", "</", "<\\", "<@?", "<@", "<\\", "<:b", "<a:"]
		
		if ("<>" in message.content or message.content.startswith("<") and message.content.endswith(">")):
			for block in black_list:
				if block in message.content or message.content.startswith(block):
					return
			value = message.content.strip("<>").strip()
			try:
					card = Card(card=cards_data[cards_id[str(value)]])
					await message.reply(embed=await card.embed_cards())
			except:
				value = await self.clean(value)
				name = await self.fuzzy(value, [n for n in cards_name if value in n], results=1)
				try:
					card = Card(card=cards_data[name[0]])
					await message.reply(embed=await card.embed_cards())
				except:
					await message.add_reaction("❓")
					await self.NoResult(message=message)
		else:
				return
	
	#function return if not found card
	async def NoResult(self, interaction: Interaction=None, message=None):
		
		try:
			if interaction is not None:
				await interaction.response.send_message(embed=Embed(color=config["embed-color"], description=">>> **No results found, please try again**"))
				return
			elif message is not None:
				await message.reply(embed=Embed(color=config["embed-color"], description=">>> **No results found, please try again**"))
				return
			else:
				return
		except:
			pass
	
	
	#function check and return a news cards and send to guild channels 
	async def NewCards(self, new_cards):
				
				settings = Load("settings.json")
				channel = await self.bot.fetch_channel(settings["cards_news"])
				
				for name in new_cards:
						try:
							card = Card(card=cards_data[name])
							await channel.send(embed=await card.embed_new_cards())
						except:
							continue
			
	
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
		