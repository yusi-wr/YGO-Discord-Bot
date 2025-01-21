from nextcord.ext.commands import Bot
from database import tournaments
import os
from . import Functions, ClassButtonTournament, ClassViewLog_Info
from database import tickets
from .tickets.views import ViewSettingsTicket
from .tickets.embeds import embed_reply
from colorama import Fore
from .tournaments.embeds import embed_log

class ViewUpdates:
	def __init__(self, bot: Bot):
		self.bot = bot
		self.help_functions = Functions(self.bot)
	
	#Run functions ^_^
	async def Run(self):
		
		print(Fore.LIGHTMAGENTA_EX + " • View Update: " + Fore.LIGHTGREEN_EX + "Start" + Fore.RESET)
		
		await self.Tournaments() #run function update view tournaments
		await self.UserTicketUpdate() #run function update tickets
	
	#-----------------------
	
	async def Tournaments(self):
		"""view tournaments update"""
		try:
			for file in os.listdir("./database/data/tournaments/"):
				if file.endswith(".json"):
					user = await self.bot.fetch_user(int(file[:-5]))
					if user :
						data = tournaments.Load(user)
						
						guild = await self.bot.fetch_guild(data["guild"])
						channel_announce = await self.bot.fetch_channel(data["channel_announce"])
						log_channel = await guild.fetch_channel(data["log_channel"])
						role = guild.get_role(data["role"])
						msg_announce = await channel_announce.fetch_message(data['msg_announce'])
						
						
						is_started = data["is_started"]
						name = data["name"]
						
						if not is_started == True:
							await msg_announce.edit(view=ClassButtonTournament(Manager=user, name=name, chat_announce=channel_announce, bot=self.bot, role=role))
						else:
							await msg_announce.edit(f"{role.mention}", embed=embed_log(manager=user), view=ClassViewLog_Info(manager=user, bot=self.bot))
		except AttributeError as Error:
			await self.help_functions.log_errors(errorLog=f"```{Error}```")
			
	
	#ticket opened update
	async def UserTicketUpdate(self):
			
			try:
				for file in os.listdir("./database/data/tickets/"):
					if file.endswith(".json"):
						user = await self.bot.fetch_user(int(file[:-5]))
						data = tickets.Load(user)
						channel = await self.bot.fetch_channel(data["channel"])
						message = await channel.fetch_message(data["msg"])
						if not message or not user or not channel:
							os.remove(f"./database/data/tickets/{file}")
							if channel:
								await channel.delete()
								continue
						elif user not in channel.guild.members:
							os.remove(f"./database/data/tickets/{file}")
							try:
								await user.send(embed=embed_reply(f"Hello my friend {user.mention}\nYou have previously opened a ticket on the `{channel.guild.name}` server\nWell the ticket will be automatically deleted due to your not being on the server"))
							except:
								pass
							continue
						
						if message:
							await message.edit(view=ViewSettingsTicket(user=user, bot=self.bot))
						
					else:
						continue
			except AttributeError as Error:
				await self.help_functions.log_errors(errorLog=f"```{Error}```")
			
		
		
	