from .icons_colors import icon, colors_types
from .data import cards_art, cards_images
import os
from urllib.parse import quote
from nextcord import Embed
from config import config
import requests
import asyncio
import aiohttp

emote = config["emoji"]

def Level_Scale(card):
	if "xyz" in card["type"].lower():
		level= f"\n**Rank**: {icon['level']['rank']} {card['level']}"
	elif "link" in card["type"].lower():
		level= f"\n**Link**: {icon['level']['link']} {card['linkval']}"
	else:
		level= f"\n**LeveL**: {icon['level']['level']} {card['level']}" if "Monster" in card["type"] else ""
		
	sclae = f" | **Scale** {icon['scale']} {card['scale']}" if "scale" in card else ""
	return f"{level}{sclae}"

def Banlist(card):
		
	banlist = card["banlist_info"] if "banlist_info" in card else ""
	ban_tcg = banlist["ban_tcg"] if "ban_tcg" in banlist else "Unlimited"
	ban_ocg = banlist["ban_ocg"] if "ban_ocg" in banlist else "Unlimited"
	
	formats = card["misc_info"][0]["formats"]
	if "TCG" not in formats:
		ban_tcg = "N/A"
	if "OCG" not in formats:
		ban_ocg = "N/A"
	
	return f"**Limit**: TCG {icon['banlist'][ban_tcg]} | OCG {icon['banlist'][ban_ocg]}\n"

def type_cards(card):
	
	if "Monster" in card['type']:
		mtype = str(card["type"]).replace("Monster", "").strip().replace(" ", " / ")
		tp = f"**Type**: {icon['race'][card['race']] if card['race'] in icon['race'] else card['race']} / {mtype} / {card['attribute']}"
	elif "Trap" or "Spell" in card["type"]:
		tp = f"**Type**: {icon['race'][card['race']] if card['race'] in icon['race'] else card['race']} {card['type'].replace('Card', '').strip()}"
	else:
		tp = f"**Type**: {card['type']}"
	return tp

class Card:
	def __init__(self, card):
		self.card = card
		
		self.level = Level_Scale(card)
		self.type = type_cards(card)
		self.banlist = Banlist(card)
		self.color_card = colors_types[card["type"]] if card["type"] in colors_types else 0x414645
		self.name = card["name"]
		self.desc = card["desc"]
		self.id = card["id"] if "id" in card else "???????"
		self.url = card["ygoprodeck_url"]
		self.archetype = f"\n**Archetype**: {card['archetype']}" if "archetype" in card else ""
		
		if "Monster" in card["type"]:
			if "Link" in card["type"]:
				self.atk_def = f"\n**ATK**: {card['atk']}"
			else:
				self.atk_def = f"\n**ATK**: {card['atk']} / **DEF**: {card['def']}"
		else:
			self.atk_def = ""
		
		if "Monster" in card["type"]:
			self.attribute = f"{icon['icon_url'][card['attribute']] if card['attribute'] in icon['icon_url'] else ''}"
		elif "Spell" or "Trap" in card["type"]:
			self.attribute = f"{icon['icon_url'][card['type'].replace('Card', '').strip()] if card['type'].replace('Card', '').strip() in icon['icon_url'] else ''}"
		else:
			self.attribute = ""
		self.misc_info = card["misc_info"] if "misc_info" in card else ""
		
		try:
				self.konamiID = self.misc_info[0]["konami_id"]
		except:
				self.konamiID = "0000"
		
		self.links = f"**[Master duel](https://www.masterduelmeta.com/cards/{quote(self.name)}) / [Decks](https://ygoprodeck.com/deck-search/?&name={quote(self.name)}&offset=0) / [Meta Decks](https://ygoprodeck.com/deck-search/?&name={quote(self.name)}&_sft_category=meta%20decks&offset=0) / [Yugipedia](https://yugipedia.com/wiki/{self.konamiID}) / [Konami DB](https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=2&request_locale=en&cid={self.konamiID})**"
		
	async def embed_cards(self):
		
		embed = Embed(color=self.color_card)
		embed.description = f"{self.banlist}{self.type}{self.archetype}{self.level}{self.atk_def}"
		embed.set_author(name=self.name, icon_url=self.attribute, url=self.url)
		embed.add_field(name="**Effect**", value=f">>> *{self.desc}*")
		embed.set_thumbnail(url=cards_art[self.id]["url"])
		embed.set_footer(text=f"Password: {self.id} | Konami ID #{self.konamiID} | Developed by: Y/W", icon_url=config["icon"])
		#embed.add_field(name=f"**{emote['list']} Banlists**", value=f">>> ")
		embed.add_field(name=f"**{emote['link']} Links**", value=f">>> {self.links}")
		
		return embed
	
	async def embed_arts(self):
		
		embed = Embed(color=self.color_card)
		embed.set_author(name=self.name, icon_url=self.attribute, url=self.url)
		embed.set_image(url=cards_art[self.id]["url"])
		embed.set_footer(text=f"Password: {self.id} | Konami ID #{self.konamiID} | Developed by: Y/W", icon_url=config["icon"])
		
		return embed
		
	async def embed_normal_images(self):
		
		embed = Embed(color=self.color_card)
		embed.set_author(name=self.name, icon_url=self.attribute, url=self.url)
		embed.set_image(url=cards_images[self.id]["url"])
		embed.set_footer(text=f"Password: {self.id} | Konami ID #{self.konamiID} | Developed by: Y/W", icon_url=config["icon"])
		
		return embed
		
	async def embed_new_cards(self):
		
		embed = Embed(color=self.color_card)
		embed.description = f"{self.banlist}{self.type}{self.archetype}{self.level}{self.atk_def}"
		embed.set_author(name=self.name, icon_url=self.attribute, url=self.url)
		embed.add_field(name="**Effect**", value=f">>> *{self.desc}*")
		try:
			embed.set_image(url=cards_images[self.id]["url"])
		except:
			embed.set_thumbnail(url=cards_art[self.id]["url"])
		embed.set_footer(text=f"Password: {self.id} | Konami ID #{self.konamiID} | Developed by: Y/W", icon_url=config["icon"])
		#embed.add_field(name=f"**{emote['list']} Banlists**", value=f">>> ")
		#embed.add_field(name=f"**{emote['link']} Links**", value=f">>> {self.links}")
		
		