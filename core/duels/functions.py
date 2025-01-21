from database import challenges, users
from config import config
from nextcord.ext import commands
from nextcord import User
from datetime import datetime

emote = config["emoji"]

class FunctionsHelp:
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	#save users duels
	def ScoreDuel_Save(self, player: User, is_winner=True, score_text=""):
		
		time = str(datetime.utcnow()).split(".")[0].replace("-", "/")
		duelData = users.Duels_Data(player)
		duelData["duels"][time] = score_text
		
		userData = users.Load(player)
		userData["duels"]["count"] += 1
		if is_winner == True:
			userData["duels"]["win"] += 1
		else:
			userData["duels"]["lose"] += 1
			
		users.Duels_Update(player, duelData)
		users.Update(player, userData)
			
		
	