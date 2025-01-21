from nextcord import Interaction, User, Message, CategoryChannel, Embed, Member
from nextcord.ext import commands
from database import users, tickets, Load, data_dir
from config import config
import os
from .embeds import embed_reply
from random import randint

emote = config["emoji"]

class TicketFunction:
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		
	#setup a new tickets and save to data
	async def setup(self, message: Message, category: CategoryChannel, channel, is_free):
		
		data = {}
		data["guild"] = message.guild.id
		data["category"] = category.id
		data["channel"] = channel.id
		data["is_free"] = is_free
		
		tickets.Setup_Save(message, data)
	
	#check ticket setup
	async def claer_setup(self):
		
		try:
			for file in os.listdir(f"{data_dir}tickets/setup/"):
				if file.endswith(".json"):
					data = Load(file=f"tickets/setup/{file}")
					guild = await self.bot.fetch_guild(data["guild"])
					channel = await guild.fetch_channel(data["channel"])
					message = await channel.fetch_message(int(file[:-5]))
					
					tickets.Setup_Delete(file=file)
					try:
						await message.edit(embed=embed_reply(f"We apologize to everyone. The ticket activity has been cancelled. You cannot open a ticket at this time °_°"))
					except:
						continue
		except:
			pass
			
	#clear tickets		
	async def clear_tickets(self, reason="None...."):
			
			try:
				count = 0
				for file in os.listdir(f"{data_dir}tickets/"):
					if file.endswith(".json"):
						user = await self.bot.fetch_user(file[:-5])
						data = tickets.Load(user)
						channel = await self.bot.fetch_channel(data["channel"])
						if channel:
							await channel.delete()
						embed = embed_reply(desc=f"Your ticket and ticket list have been deleted by the server administration. We apologize for that\n- Reason: ```{reason}```")
						try:
							await user.send(f"{user.mention}", embed=embed)
						except:
							pass
						tickets.Delete(user)
						count += 1
				return count
			except:
				return None
			
	#--------------------------(other function for  help)
	
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
			