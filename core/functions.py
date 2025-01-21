import nextcord
from nextcord.ext import commands, tasks
from nextcord import Embed, Interaction, Member, User, Guild, Color, TextChannel, File, utils
import random, humanfriendly
import time as pyTime
from config import config
from database import Load, Update, data_dir
from datetime import datetime, timedelta
from .views import DailyGifts, Verify, ButtonGames
from .tickets.views import ViewTickets
import os
import asyncio

context = commands.Context
emote = config["emoji"]
#embed
def ErrorEmbed(desc):
	
	embed = Embed(color=config["embed-color"])
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1180266906314346677/1185547458160373820/Picsart_23-12-16_09-43-27-780.png")
	embed.title = f"**{emote['no']} Warning**"
	embed.description = f">>> **{desc}**"
	embed.set_author(name=config["name"], icon_url=config["icon"])
	
	return embed
	
class Functions:
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	#function add view
	def Add_View(self):
		#self.bot.add_view(DailyGifts(self.bot))
		self.bot.add_view(ViewTickets(self.bot))
		self.bot.add_view(ButtonGames())
	
	#what is user rank
	def RankCall(self, points):
		rank = emote["ranks"]
		
		if points >= 0 and not points >= 60:
			return rank["iron"]
		elif points >= 60 and not points >= 160:
			return rank["bronze"]
		elif points >= 150 and not points >= 260:
			return rank["silver"]
		elif points >= 260 and not points >= 380:
			return rank["gold"]
		elif points >= 380 and not points >= 510:
			return rank["platinum"]
		elif points >= 510 and not points >= 720:
			return rank["daimond"]
		elif points >= 720 and not points >= 1230:
			return rank["master"]
		elif points >= 1230:
			return rank["legend"]
		else:
			return rank["noob"]
	
	#embed for use any time	
	def embed(self, desc, title = None, icon = None, img=None):
		embed = Embed(color=config["embed-color"])
		embed.description = f">>> **{desc}**"
		embed.title = title
		embed.set_author(name=config["name"], icon_url=config["icon"])
		if img:
			embed.set_image(url=img)
		if icon:
			embed.set_thumbnail(url=icon)
			
		return embed
	
	#check user is in guild and return None if not
	def Check_in_guild(self, user: User, guild: Guild):
		
		return True if user in guild.members else False
	
	# check use has role any admins role
	def CheckPermisions(self, user: Member, is_owner_only=False):
		
		settings = Load("settings.json")
		guild = user.guild
		if is_owner_only:
			if user.id not in settings["owners"]:
				return False
			else:
				return True
			
		else:
			roles = [guild.get_role(x) for x in settings["admins"]]
			
			if len(roles) > 0:
				if any(role in user.roles for role in roles)  or user.id in settings["owners"]:
					return True
				else:
					return False
			else:
				if user.id in settings["owners"]:
					return True
				else:
					return False
	
	#function command cooldwon
	def check_cooldwon(self, user: Member, command):
		
		if f"{str(user.id)}.json" not in os.listdir("./database/data/cooldwons/"):
			data = {}
			Update(file=f"cooldwons/{str(user.id)}.json", data=data)
			
		data = Load(f"cooldwons/{str(user.id)}.json")
		
		if command not in data:
			data[command] = str(datetime.utcnow())
			Update(file=f"cooldwons/{str(user.id)}.json", data=data)
			return True
		else:
			dateNow = data[command]
			date = datetime.strptime(dateNow, "%Y-%m-%d %H:%M:%S.%f")
			diff = datetime.utcnow() - date
			
			if (diff.total_seconds() / 3600) >= 24:
				data[command] = str(datetime.utcnow())
				Update(file=f"cooldwons/{str(user.id)}.json", data=data)
				return True
			else:
				return False
	
	#get user time of cooldwon
	def get_cooldwon(self, user: Member, command):
			
			data = Load(f"cooldwons/{str(user.id)}.json")
			
			UserDate = data[command]
			getdate = datetime.strptime(UserDate, "%Y-%m-%d %H:%M:%S.%f")
			diff = datetime.utcnow() - getdate
			date = str(timedelta(seconds=86400 - diff.total_seconds())).split(".")[0]
			
			return date
	
	#--------------------------------(aysnc func ↓)
	
	#func for use any time send line image to any channel
	async def Send_line_Image(self, channel: TextChannel, img):
		file_image = f"./assets/{img}"
		send = await channel.send(file=File(file_image))
		await send.edit("@here")
	
	#function welcome and verify
	async def Welcome(self, user: Member, guild: Guild):
		
		settings = Load("settings.json")
		channel = guild.system_channel
		role = guild.get_role(settings["welcome_role"])
			
		embed = Embed(color=config["embed-color"])
		embed.title = f"{emote['welcome']} **Welcome** {emote['welcome']}"
		embed.set_author(name=config["name"] + " | Welcome", icon_url=config["icon"])
		embed.set_thumbnail(url=user.avatar.url)
		embed.set_image(url=config["img"]["bg-welcome"])
		
		if user.id in Load("verifiy.json")["users"]:
			embed.description = f">>> **- Welcome back {user.mention}. I am happy to have you with us again at `{guild.name}`**"
			
			if channel:
				await channel.send(f"• {user.mention} •",embed=embed)
				await user.add_roles(role)
				
		else:
			embed.description = f">>> **- Welcome {user.mention}\n- Welcome to `{guild.name}`\n- We hope you have a wonderful and enjoyable time with us**"
			if channel:
				await channel.send(f"• {user.mention} •", embed=embed, view=Verify(user=user, role=role))
			
	# error on slash_command
	async def ErrorSlash(self, errorLog, interaction: Interaction):
	
		try:
			await interaction.followup.send(embed=ErrorEmbed(desc=errorLog))
		except:
			await interaction.message.edit(embed=ErrorEmbed(desc=errorLog))
	
	# error prefix_command
	async def ErrorPrefix(self, errorLog, ctx: commands.Context):
	
		await ctx.reply(embed=ErrorEmbed(errorLog))
	
	#log errors 	
	async def log_errors(self, errorLog):
	
		settings = Load(file="settings.json")
		
		channel = await self.bot.fetch_channel(settings["log-channel"])
		owner = await self.bot.fetch_user(self.bot.owner_id)
		
		await channel.send(f"**{owner.mention}**", embed=ErrorEmbed(errorLog))
	
	#
	async def NonHasPermisions(self, ctx: commands.Context= None, interaction: Interaction=None):
		
		if interaction is not None:
			await self.ErrorSlash(errorLog="Sorry, you do not have permission to use this command", interaction=interaction)
			return
		elif ctx is not None:
			await self.ErrorPrefix(errorLog="Sorry, you do not have permission to use this command", ctx=ctx)
			return
		else:
			return