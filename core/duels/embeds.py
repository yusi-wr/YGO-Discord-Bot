from nextcord import Embed, User
from config import config
from database import users, challenges

emote = config["emoji"]

#embed challenge after confirmed and start
def embed_challenge_start(player, opponent, points):
	
	embed = Embed(color=config["embed-color"])
	embed.title = "**Duel challenge**"
	embed.description = f">>> **The challenge has been registered\n- {player.mention} {emote['vs']} {opponent.mention}\n Please inform any admin when the challenge match ends**"
	embed.add_field(name="**Challenge points**", value=f">>> - {emote['points']} {points}")
	embed.set_image(url="https://cdn.discordapp.com/attachments/1180266906314346677/1246818775681073362/yugioh_master_duel_copertina.jpg")
	embed.set_author(name=config["name"] + " | Challenge duels", icon_url=config["icon"])
	embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/761250789011488770.png")
	
	return embed
	
	
#embed cancel challenges
def embed_cancel_challenge(player, opponent, points):
	
	embed = Embed(color=config["embed-color"])
	embed.description = f">>> **The challenge has been canceled due to the player not agreeing {opponent.mention}\n {player.mention} please look for another player**"
	embed.add_field(name="**Challenge points**", value=f">>> - {emote['points']} {points}")
	embed.set_author(name=config["name"] + " | Challenge duels", icon_url=config["icon"])
	embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/900307864156004353.png")
	
	return embed


def embed_challenge_end(winner: User, loser: User, score_text, points):
	
	embed = Embed(color=config["embed-color"])
	embed.description = f">>> **Confirm the challenge has finished\n{emote['score']} *Match score*\n{score_text}\n\nPrize of duel\n{winner.mention}\n- Win: {emote['points']} {points}\n{loser.mention}\n- Lose: {emote['points']} {points}**"
	embed.set_author(name=config["name"] + " | Challenge duels", icon_url=config["icon"])
	embed.set_image(url=config["img"]["bg-duel"])
	
	return embed
	
def embed_normal_duels(winner: User, loser: User, score_text, prize):
	
	embed = Embed(color=config["embed-color"])
	embed.description = f">>> **{emote['duel']} Normal duels\n{emote['score']} *Match score*\n{score_text}\n\- Prize\n{prize}**"
	embed.set_author(name=config["name"] + " | Duels", icon_url=config["icon"])
	embed.set_image(url=config["img"]["bg-duel"])
	
	return embed
	

def embed_duel_history(player: User):
	
	data = users.Load(player)
	embed = Embed(color=config["embed-color"])
	embed.title = f"**{data['nickname']}**" if data["nickname"] != None else f"**{player.name}**"
	embed.description = f">>> **{emote['duel']} Duels historys\n- Results do not include tournaments, only Normal/Challenges\n- Unwanted dates can be deleted using: `?delete-history`**"
	embed.set_author(name=config["name"] + " | Duels", icon_url=config["icon"])
	embed.set_image(url=config["img"]["bg-duel"])
	
	return embed


def embed_challenge_delete(player: User, opponent: User, points, author: User):
	
	embed = Embed(color=config["embed-color"])
	embed.description = f">>> **- Delete the challenge By: {author.mention}\n- {emote['duel']} Players\n{emote['score']} {player.mention} {emote['vs']} {opponent.mention}\n\n- Challenge points\n{emote['points']} `{points}`**"
	embed.set_author(name=config["name"] + " | Duels", icon_url=config["icon"])
	embed.set_image(url=config["img"]["bg-duel"])
	
	return embed
	
def embed_challenge_show(player: User, opponent: User, points):
	
	embed = Embed(color=config["embed-color"])
	embed.title = f"** {emote['star']} Challenge duel {emote['star']}**"
	embed.description = f">>> **{emote['score']} Match\n- {player.mention} {emote['vs']} {opponent.mention}\n- Created by: {player.mention}\n- Challenge points\n- {emote['points']} {points}**"
	embed.set_author(name=config["name"] + " | Challenge duels", icon_url=config["icon"])
	embed.set_image(url=config["img"]["bg-duel"])
	
	return embed
	
def embed_reply(desc):
	
	embed = Embed(color=config["embed-color"])
	embed.description = f">>> **{desc}**"
	embed.set_author(name=config["name"] + " | duels", icon_url=config["icon"])
	embed.set_image(url=config["img"]["bg-duel"])
	
	return embed