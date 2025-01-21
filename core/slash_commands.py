from nextcord import TextChannel, Member, Interaction, Role, Embed, Message, Attachment
from nextcord.ext import commands
from database import Load, Update, users
from config import config, loading
from .views import ButtonGames
from . import Functions
from random import randint
emote = config["emoji"]

class Slash_Command:
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.functions = Functions(self.bot)
	
	
	
	#set nickname for profile
	async def ChangeNickName(self, interaction: Interaction, nickname: str):
		
		send = await interaction.response.send_message(embed=loading)
		
		user = interaction.user
		data = users.Load(user)
		price = randint(3500, 5500)
		
		if data["gems"] < price:
			await self.functions.ErrorSlash(errorLog=f"Sorry you don't have enough gems to change the nickname you need up to {emote['gems']} {5500:,} gem", interaction=interaction)
			return
			
		data['nickname'] = str(nickname)
		users.Update(user, data)
		
		embed = self.functions.embed(
		  desc=f"{emote['yes']} The NickName was changed successfully. \n- You paid: {emote['gems']} {price}",
		  title=" • Set Nickname`s"
		)
		
		await send.edit(embed=embed)
		
	
	#function set backgrounds
	async def ChangeBG(self, interaction: Interaction, bg: Attachment=None, img_url=None):
		
		send = await interaction.response.send_message(embed=loading)
		
		user = interaction.user
		data = users.Load(user)
		price = randint(4000, 7500)
		
		if data["gems"] < price:
			await self.functions.ErrorSlash(errorLog=f"Sorry you don't have enough gems to change the background you need up to {emote['gems']} {7500:,} gem", interaction=interaction)
			return
			
		if bg:
			bg_url = bg.url
		else:
			bg_url = img_url
		data["bg"] = str(bg_url).split("?ex")[0] if "?ex" in bg_url else str(bg_url)
		data["gems"] -= price
		users.Update(user, data)
		
		embed = self.functions.embed(
		  desc=f"{emote['yes']} The background was added successfully. \n- You paid: {emote['gems']} {price}",
		  title=" • Set background`s"
		)
		
		await send.edit(embed=embed)
	
	
	#function set backgrounds
	async def ChangeProfile(self, interaction: Interaction, bg: Attachment=None, img_url=None):
		
		send = await interaction.response.send_message(embed=loading)
		
		user = interaction.user
		data = users.Load(user)
		price = randint(4000, 6900)
		
		if data["gems"] < price:
			await self.functions.ErrorSlash(errorLog=f"Sorry you don't have enough gems to change the profile icon you need up to {emote['gems']} {6900:,} gem", interaction=interaction)
			return
			
		if bg:
			bg_url = bg.url
		else:
			bg_url = img_url
		data["icon"] = str(bg_url).split("?ex")[0] if "?ex" in bg_url else str(bg_url)
		data["gems"] -= price
		users.Update(user, data)
		
		embed = self.functions.embed(
		  desc=f"{emote['yes']} The profile icon was added successfully. \n- You paid: {emote['gems']} {price}",
		  title=" • Set profile icon`s"
		)
		
		await send.edit(embed=embed)
		
	#for admin send a normal message
	async def AdminMessage(self, interaction: Interaction, message: str, channel: TextChannel=None, is_for_new =None):
		
		send = await interaction.response.send_message(embed=loading, ephemeral=True)
		if channel:
			if is_for_new == "news":
				await self.functions.Send_line_Image(channel, "news.png")
			else:
				await self.functions.Send_line_Image(channel, "line.png")
			await channel.send(f">>> {message}\n- @here")
			await self.functions.Send_line_Image(channel, "line.png")
		else:
			await interaction.channel.send(f"{message}")
		
		await send.edit(embed=self.functions.embed(desc=f"{emote['yes']} Done successfuly"))
	
	
	#function command send embed
	async def AdminEmbed(self, interaction: Interaction,
	   title: str,
	   desc: str,
	   img = None,
	   channel: TextChannel = None,
	   is_for_new = "normal"
	):
		send = await interaction.response.send_message(embed=loading, ephemeral=True)
		settings = Load("settings.json")
		embed: Embed = self.functions.embed(
		  desc=desc,
		  title=title,
		  icon=config["icon"],
		  img = img if img else config["img"]["bg"]
		)
		embed.set_footer(text=f"Sended by: {interaction.user.display_name} | {config['name']}")
		
		if channel:
			if is_for_new == "news":
				await self.functions.Send_line_Image(channel, "news.png")
			else:
				await self.functions.Send_line_Image(channel, "line.png")
			await channel.send(f"{settings['bot-mention']}", embed=embed)
			await self.functions.Send_line_Image(channel, "line.png")
		else:
			await interaction.channel.send(embed=embed)
		
		await send.edit(embed=self.functions.embed(desc=f"{emote['yes']} Done successfuly"))
	
	
	async def RoleGameButtons(self, interaction: Interaction, channel: TextChannel):
		
		send_loading = await interaction.response.send_message(embed=loading, ephemeral=True)
		
		embed = Embed(color=config["embed-color"])
		embed.title = "**Yu-Gi-Oh Games Roles 🐇**"
		embed.description = f"**Press the button that bears the name of the game. More than one role can be selected according to the game.**"
		embed.set_author(name=config["name"] + " | Games roles", icon_url=config["icon"])
		embed.set_footer(text="click to add role and again for remove")
		embed.set_thumbnail(url=config["icon"])
		embed.set_image(url=config["img"]["bg"])
		
		await self.functions.Send_line_Image(channel, "line.png")
		send = await channel.send(embed=embed, view=ButtonGames())
		await self.functions.Send_line_Image(channel, "line.png")
		await send.edit("@here")
		
		await send_loading.edit(embed=self.functions.embed(desc=f"{emote['yes']} Done successfuly"))
	
	
	#functon settings slash command
	async def Settings(self, interaction: Interaction,
	    set_admin: Role = None,
	    remove_admin: Role = None,
	    tournament_channel: TextChannel = None,
	    channel_log: TextChannel = None,
	    bot_mention = None,
	    daliygift_channel = None,
	    welcome_role = None,
	    cards_news = None,
	    daily_gifts = None
	):
		
		settings = Load(file="settings.json")
		if channel_log is not None:
			settings["log-channel"] = channel_log.id
		if bot_mention is not None:
			settings["bot-mention"] = bot_mention
		if set_admin is not None:
			if "admins" not in settings:
				settings["admins"] = []
				settings["admins"].append(set_admin.id)
			else:
				settings["admins"].append(set_admin.id)
		if remove_admin is not None:
			if remove_admin.id in settings["admins"]:
				settings["admins"].remove(remove_admin.id)
		if daliygift_channel is not None:
			settings["daliygift"] = daliygift_channel.id
		if welcome_role is not None:
			settings["welcome_role"] = welcome_role.id
		if cards_news is not None:
			settings["cards_news"] = cards_news.id
		if daily_gifts is not None:
			settings["daily_gifts"] = daily_gifts
		
		
		if any([channel_log, bot_mention,set_admin, remove_admin, daliygift_channel, welcome_role, cards_news, daily_gifts]):
			owners = config["owners"]
			owner = interaction.guild.owner
			owners.append(owner.id) if owner.id not in owners else None
			settings["owners"] = owners
			Update(file="settings.json", data=settings)
	
			await interaction.response.send_message(f">>> {emote['yes']} **Settings have been added successfully. Thank you**", ephemeral=True)
		else:
			await interaction.response.send_message("**Nothing has been specified to change**", ephemeral=True)