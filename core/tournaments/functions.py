from nextcord.ext import commands
from config import config
from nextcord import TextChannel, Role, User
from database import tournaments, Load, users
from .embeds import *
from .views import ClassButtonTournament as ButtonTourna
from .views import ClassViewLog_Info
import os
from random import randint


class FunctuonsTourna:
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.tourn_data = tournaments
		from core import Functions
		self.functions = Functions(self.bot)
	
	#function help for save a new tournaments data
	def CreateSaveTournaData(self, Manger: User, name: str,channel_announce: int, msg_announce, role: int, log_channel, guild):
		
		data = {}
		data["channel_announce"] = channel_announce
		data["msg_announce"] = msg_announce
		data["log_channel"] = log_channel
		data["name"] = name
		data["role"] = role
		data["guild"] = guild
		data["round"] = 0
		data["is_started"] = False
		data["participants"] = []
		data["current-round"] = []
		data["next-round"] = []
		data["leave"] = []
		data["log"] = {}
		
		self.tourn_data.Update(Manger, data)
	
	#
	def MatchPrize(self, player, is_winner):
		
		data = users.Load(player)
		
		if is_winner is not True:
				dp = randint(1, 5)
				gems = randint(800, 1000)
				data["duels"]["lose"] += 1
				data["duels"]["count"] += 1
		else:
				dp = randint(5, 10)
				gems = randint(1000, 2000)
				data["duels"]["win"] += 1
				data["duels"]["count"] += 1
				
		data["dp"] += dp
		data["gems"] += gems
		users.Update(player, data)
		
		return f"- {emote['gems']} {gems:,}\n- {emote['points']} {dp}"
		
		
	#------------------------------------------------------------
	
	#function help for end tournament
	async def EndTourna(self, manager, data, winner, winner2, winner3 = None):
		
		guild = await self.bot.fetch_guild(data["guild"])
		channel_announce = await guild.fetch_channel(data["channel_announce"])
		channel_log =await guild.fetch_channel(data["log_channel"])
		role = guild.get_role(data["role"])
		msg_announce = await channel_announce.fetch_message(data["msg_announce"])
		
		embed_logs = embed_log_all(data, winner_of_tournament=winner, manager=manager)
		embed_finals = await embed_final(bot=self.bot, manager=manager, winner=winner, winner2=winner2, winner3=winner3)
		await msg_announce.edit(f"• {role.mention} | @here •", embeds=[embed_finals, embed_logs], view=None)
		await msg_announce.reply(f"{role.mention} | {channel_log.mention}")
		
		dataWinner = users.Load(winner)
		dataWinner["cup"] += 1
		users.Update(user=winner, data=dataWinner)
		
		os.remove(f"./database/data/tournaments/{str(manager.id)}.json")
		await role.delete()
	
	
	#remove user participants list
	async def RemovePlayer(self, manager: User, user: User):
		
		data = self.tourn_data.Load(manager)
		if user.id in data["participants"]:
			data["participants"].remove(user.id)
			guild = await self.bot.fetch_guild(data["guild"])
			role = guild.get_role(data["role"])
			await user.remove_roles(role)
			self.tourn_data.Update(manager, data)
	
	#save result any matchs in the tournaments to log
	async def ResultMatchSave(self, manager: User, log_match, winner: User, loser: User):
		
		data = self.tourn_data.Load(manager)
		round = str(data["round"])
		
		log = data["log"]
		if round in log:
			data["log"][round].append(log_match)
		else:
			data["log"][round] = []
			data["log"][round].append(log_match)
			
		data["current-round"].remove(winner.id)
		data["current-round"].remove(loser.id)
		data["next-round"].append(winner.id)
		data["leave"].append(loser.id)
		self.tourn_data.Update(manager, data)
	
	
	#function create tournament
	async def CreateTournament(self, manager: User, name: str, desc: str, channel_announce: TextChannel, role: Role, log_channel: TextChannel):
		"""Function create tournaments"""
		
		settings = Load(file="settings.json")
		guild = channel_announce.guild
		embed = embed_tounaments(desc=desc, name=name, manager=manager)
		
		await self.functions.Send_line_Image(channel_announce, "tourna.png")
		msg = await channel_announce.send(f"{settings['bot-mention']}", embed=embed, view=ButtonTourna(Manager=manager, name=name, chat_announce=channel_announce, bot=self.bot, role=role))
		await self.functions.Send_line_Image(channel_announce, "line.png")
		
		self.CreateSaveTournaData(Manger=manager, name=name, channel_announce=channel_announce.id, msg_announce=msg.id, role=role.id, log_channel=log_channel.id, guild=guild.id)
		
	#simple function
	async def format_matches(self, participants: list):
	     '''format the duel and return Player vs Player2'''
	     matches = [] 
	     for i in range(0, len(participants), 2):
	     	matches.append((participants[i], participants[i + 1]))
	     	
	     result = ""
	     for match in matches:
	     		result += f"{match[0]} {emote['vs']} {match[1]}\n"		
	     return result
	
	async def Start_Round(self, manager: User):
		'''Function for start the next round'''
		data = self.tourn_data.Load(manager)
		
		async def function(participants, round):
			result_lot = await self.format_matches(participants)
			
			embed = embed_rounds(desc=result_lot, manager=manager, name=data["name"], round=round)
			
			channel_annouce = await self.bot.fetch_channel(data["channel_announce"])
			log_channel = await self.bot.fetch_channel(data["log_channel"])
			msg_announce = await channel_annouce.fetch_message(data["msg_announce"])
			role = channel_annouce.guild.get_role(data["role"])
			
			await msg_announce.edit(embed=embed, view=ClassViewLog_Info(manager, self.bot))
			await channel_annouce.send(f"{role.mention}", delete_after=25)
			
		async def fetch_players(players_list: list):
			players = []
			for user_id in players_list:
				player = await self.bot.fetch_user(user_id)
				players.append(player.mention)
				
			return players
			
		if data["is_started"] == False:
			
			for num in range(len(data["participants"])):
				for user_id in data["participants"]:
					data["current-round"].append(user_id)
					data["participants"].remove(user_id)
			participants = data["current-round"]
			
			await function(await fetch_players(participants), 1)
			
			if "1" not in data["log"]:
				data["log"]["1"] = []
			data["round"] += 1
			data["is_started"] = True
			self.tourn_data.Update(manager, data)
			
		else:
			for num in range(len(data["next-round"])):
				for user_id in data["next-round"]:
					data["current-round"].append(user_id)
					data["next-round"].remove(user_id)
					
			if len(data["current-round"]) == 2:
				data["round"] = "final"
			
			await function(await fetch_players(data["current-round"]), data["round"])
			
			num_log = str(data["round"])
			if num_log not in data["log"]:
				data["log"][num_log] = []
			if data["round"] != "final":
				data["round"] += 1
			self.tourn_data.Update(manager, data)
				
			
			
			
			
			
				
		
		