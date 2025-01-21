from nextcord import Embed, User
from config import config
from database import tournaments as data_tourna
from datetime import datetime
emote = config["emoji"]

def embed_tounaments(name: str,desc: str, manager: User):
	
	embed = Embed(color=config["embed-color"])
	embed.set_author(name=config["name"] + " | Tournaments", icon_url=config["icon"])
	embed.description = f">>> **{desc}**"
	embed.title = f"**{emote['cup']} **{name}** {emote['cup']}**"
	#embed.set_thumbnail(url=config["tourna-icon"])
	embed.add_field(name=f"{emote['manager']} **Organizer**", value=f"- {manager.mention}")
	embed.set_image(url=config["img"]["tournament"])
	
	return embed
	

def embed_rounds(name: str, desc: str, manager: User, round):
	
	embed = Embed(color=config["embed-color"])
	embed.set_author(name=config["name"] + " | Tournaments", icon_url=config["icon"])
	embed.description = f"**- {emote['round']} Round: {round}\n>>> {desc}**"
	embed.title = f"**{emote['cup']} {name} {emote['cup']}**"
	embed.add_field(name=f"{emote['manager']} **Organizer**", value=f"- {manager.mention}")
	
	return embed
	
	
def embed_log_match(log_match, name, winner: User):
	  
	  embed = Embed(color=config["embed-color"])
	  embed.title= f"{emote['cup']} **{name}** {emote['cup']}"
	  embed.description = f">>> ** - {emote['score']} Match score •\n{log_match}**"
	  embed.set_image(url=config["img"]["tournament"])
	  embed.set_author(name=config["name"] + " | Tournaments", icon_url=config["icon"])
	  embed.add_field(name=f"** {emote['match-winner']} Match winner**", value=f">>> - **{winner.mention}**")
	  
	  return embed

def embed_log(manager: User):
	
	try:
		data = data_tourna.Load(manager)
		round = str(data["round"])
		round_log = data["log"][round]
		name = data["name"]
		log = "- " + "\n- ".join(x for x in round_log)
		
		embed = Embed(color=config["embed-color"])
		embed.title= f"{emote['cup']} **{name}** {emote['cup']}"
		embed.description = f"**- {emote['round']} Current round: `{round}`\n- {emote['manager']} Organizer: {manager.mention}**"
		embed.add_field(name=f"** {emote['log']} Match Log**", value=f">>> **{log}**")
		embed.set_image(url=config["img"]["tournament"])
		embed.set_footer(text=f"• 🗓️ Updated in: {str(datetime.utcnow()).split('.')[0].replace('-','/')} •")
		
		return embed
	except:
		return Embed(description="No results were found for the current round matches..........", color=config["embed-color"])

	
def embed_log_all(data, winner_of_tournament: User, manager: User):
	
	embed = Embed(color=config["embed-color"])
	#embed.description = f">>> **\n- {emote['cup-winner']} Winner: {winner_of_tournament.mention}\n- Organizer: {manager.mention}**"
	embed.title = f"**{emote['log']} Match Logs**"
	if len([x for x in data["log"]]) >= 1:
		for key in data["log"]:
			list_log = data["log"][key]
			text = ""
			for log in list_log:
				text += f"{log}\n"
					
			embed.add_field(name=f"**{emote['round']} Round: {key}**", value=f">>> **{text}**")
	else:
		embed.add_field(name=f"**{emote['round']} Log round {data['round']}**", value=f">>> - **Non any round log save....**")
	
	embed.set_image(url=config["img"]["tournament"])
		
	return embed
	
	
async def embed_final(bot, manager, winner: User, winner2: User, winner3: User = None):
	
	data = data_tourna.Load(manager)
	
	text_winner = f"- {emote['win1']} {winner.mention}\n- {emote['win2']} {winner2.mention}\n- {emote['win3']} No one..." if winner3 is None else f"- {emote['win1']} {winner.mention}\n- {emote['win2']} {winner2.mention}\n- {emote['win3']} {winner3.mention}"
	
	participants = [await bot.fetch_user(x) for x in data["leave"]]
	participants += [await bot.fetch_user(x) for x in data["next-round"]]
	if len(data["current-round"]) >= 1:
		participants += [await bot.fetch_user(x) for x in data["current-round"]]
		
	all_participants = "- " + "\n- ".join(x.mention for x in participants)
	
	embed = Embed(color=config['embed-color'])
	embed.title = f"**{emote['cup']} {data['name']} {emote['cup']}**"
	embed.description = f">>> **The tournament has ended, congratulations to the winners and thanks to the participants.\n- {emote['manager']} Organizer: {manager.mention}**"
	
	embed.add_field(name=f"• {emote['cup-winner']} Heroes", value=f">>> {text_winner}")
	embed.add_field(name=f"🫡 Thanks", value=f">>> {all_participants}")
	
	#embed.set_image(url=config["img"]["tournament"])
	embed.set_author(name=config["name"] + " | Tournaments", icon_url=config["icon"])
	
	return embed
	