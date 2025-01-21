from nextcord import Interaction, Embed, ButtonStyle
from nextcord.ui import View, Button, button
from nextcord.ext import commands
from config import config
from database import Load, users
from random import randint, choice
from datetime import datetime

emote = config["emoji"]

def embed_time_end(user_get):
	
	embed = Embed(color=config["embed-color"])
	embed.set_author(name=config["name"] + " | Gifts", icon_url=config["icon"])
	embed.title = "**Daily Gift**"
	embed.description = f">>> **The time for the daily gift has ended**"
	
	log = "\n ".join(f"{x} {user_get[x]}" for x in user_get)
	
	embed.add_field(name="**Lucky today**", value=f">>> **{log}**")
	embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1084203727637991464.png")
	embed.set_footer(text=f"Created By: Ash Blossom™ | {str(datetime.utcnow()).split('.')[0].replace('-', '/')}")
	
	return embed

class DailyGifts(View):
	def __init__(self, bot: commands.Bot, msg):
		super().__init__(timeout=1800)
		self.bot = bot
		self.msg = msg
		
		self.user_get = {}
	
	async def on_timeout(self):
		
		for button in self.children:
			button.disabled=True
			
		embed = embed_time_end(user_get=self.user_get)
		
		await self.msg.edit(embed=embed, view=self)
	
	
	@button(label="Claim", style=ButtonStyle.gray, emoji=emote["gift"], custom_id="cliamgift")
	async def ClaimButton(self, button: Button, interaction: Interaction):
			
		user = interaction.user
		data = users.Load(user)
		
		if str(user.mention) in self.user_get:
			await interaction.response.send_message(embed=Embed(color=config["embed-color"], description="**I already received the gift**"), ephemeral=True)
			return
		
		msg = await interaction.response.send_message(embed=Embed(description=f"**{emote['loading']} Loading...**"), ephemeral=True)
		
		range_gift = choice(["gem", "dp"])
		
		embed = Embed(color=config["embed-color"])
		embed.title = "**Congratulations**"
		
		if range_gift == "gem":
			gift = randint(1000, 5500)
			data["gems"] += gift
			users.Update(user, data)
			
			embed.description = f"**You have included: {emote['gems']} {gift:,}\n\nThanks ^_^**"
			text = f"{emote['gems']} {gift:,}"
		else:
			gift = randint(5, 50)
			data["dp"] += gift
			users.Update(user, data)
			
			embed.description = f"**You have included: {emote['points']} {gift:,}\n\nThanks ^_^**"
			text = f"{emote['points']} {gift:,}"
		
		self.user_get[str(user.mention)] = text
		
		await msg.edit(embed=embed)
		
		
	
		