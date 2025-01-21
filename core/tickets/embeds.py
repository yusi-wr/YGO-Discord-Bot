from nextcord import User, Embed
from config import config
from datetime import datetime
emote = config["emoji"]


#embed setup ticket
def embed_setup(desc: str, title: str, is_free="no"):
	
	embed = Embed(color=config["embed-color"])
	embed.title = f"**{title}**"
	if is_free == "yes":
		embed.description = f">>> **{desc}**"
	else:
		pay = 1200
		embed.description = f">>> **{desc}**"
		embed.add_field(name=f"**Paid ticket**", value= f">>> **- Pay: {emote['gems']} {pay:,}**")
	embed.set_image(url=config["img"]["bg"])
	embed.set_author(name=config["name"] + " | Tickets")
	embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1110797269260828695.png")
	
	return embed
	
def embed_tickets(user: User, is_free):
	
	embed = Embed(color=config["embed-color"])
	embed.set_author(name=config["name"] + " | Tickets")
	embed.set_thumbnail(url=user.avatar.url)
	embed.description = f">>> **- Welcome to your support ticket {user.mention}\n- Please wait for the server administration to respond to you**"
	if is_free != "yes":
		embed.add_field(name="**Type**", value=f">>> **- Paid ticket\n- gems: {emote['gems']} {1200:,}**")
	else:
		embed.add_field(name="**Type**", value=f">>> **- Unpaid ticket**")
	embed.set_image(url=config["img"]["bg-welcome"])
	embed.set_footer(text=f"Date: {str(datetime.utcnow()).split('.')[0].replace('-', '/')}")
	
	return embed
	

def embed_reply(desc: str):
	embed = Embed(color=config["embed-color"])
	embed.title = "**Tickets • Help**"
	embed.description = f">>> **{desc}**"
	embed.set_author(name=config["name"] + " | Tickets")
	embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1110797269260828695.png")
	#embed.set_image(url=config["img"]["bg"])
	
	return embed