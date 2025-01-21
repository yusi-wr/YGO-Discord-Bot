import json
from nextcord import User
import os

data_dir = "./database/data/"

def Load(file):
	"""For load other data"""
	return json.load(open(f"{data_dir}{file}", 'r'))
	
def Update(file, data):
	"""Update data files"""
	json.dump(data, open(f"{data_dir}{file}", 'w'), indent=2)

#class manager user data	
class Users:
	def __init__(self):
		pass
	
	#check if user have data and create is not	
	def check(self, user: User):
		
		if f"{str(user.id)}.json" not in os.listdir(f"{data_dir}users/"):
			
			data = {}
			data["nickname"] = None
			data["gems"] = 2500
			data["dp"] = 60
			data["cup"] = 0
			data["bg"] = None
			data["icon"] = None
			data["duels"] = {}
			data["duels"]["count"] = 0
			data["duels"]["win"] = 0
			data["duels"]["lose"] = 0
			
			if f"{str(user.id)}.json" not in os.listdir(f"./{data_dir}users/duels/"):
				duel_data = {}
				duel_data["duels"] = {}
				json.dump(duel_data, open(f"{data_dir}users/duels/{str(user.id)}.json", 'w'), indent=2)
			
			json.dump(data, open(f"{data_dir}users/{str(user.id)}.json", 'w'), indent=2)
	
	# load data user 
	def Load(self, user: User):
		
		self.check(user)
		return json.load(open(f"{data_dir}users/{str(user.id)}.json", 'r'))
	
	#update user data
	def Update(self, user, data):
		self.check(user)
		json.dump(data, open(f"{data_dir}users/{str(user.id)}.json", 'w'), indent=2)
		
	#load user data of duels 	
	def Duels_Data(self, user: User):
		self.check(user)
		return json.load(open(f"{data_dir}users/duels/{str(user.id)}.json", 'r'))
		
	def Duels_Update(self, user: User, data):
		self.check(user)
		json.dump(data, open(f"{data_dir}users/duels/{str(user.id)}.json", 'w'), indent=2)

#tournaments 
class Tourna:
	def __init__(self):
		pass
	# load tournaments data 
	def Load(self, user: User):
		return json.load(open(f"{data_dir}tournaments/{str(user.id)}.json", 'r'))
	
	#update tournaments data
	def Update(self, user, data):
		json.dump(data, open(f"{data_dir}tournaments/{str(user.id)}.json", 'w'), indent=2)

#challenges duel data
class Challenge:
	def __init__(self):
		pass
	
	#check 
	def check(self, player):
		
		if f"{str(player.id)}.json" not in os.listdir(f"{data_dir}challenges/"):
			return False
		else:
			return True
	
	#for create player challenge
	def Create(self, player, opponent, points):
		
		data = {}
		data["opponent"] = opponent.id
		data["points"] = points
		data["by"] = player.id
		json.dump(data, open(f"{data_dir}challenges/{str(player.id)}.json", 'w'), indent=2)
	
	# load tournaments data 
	def Load(self, player: User):
		return json.load(open(f"{data_dir}challenges/{str(player.id)}.json", 'r'))
	
	#delete data challenges
	def Delete(self, player):
		os.remove(f"{data_dir}challenges/{str(player.id)}.json")
		
		
#challenges duel data
class Tickets:
	def __init__(self):
		pass
	
	#check 
	def check(self, user):
		
		if f"{str(user.id)}.json" not in os.listdir(f"{data_dir}tickets/"):
			return False
		else:
			return True
	
	# load tickets data 
	def Load(self, user: User):
		return json.load(open(f"{data_dir}tickets/{str(user.id)}.json", 'r'))
	
	#delete data tickets
	def Delete(self, user):
		os.remove(f"{data_dir}tickets/{str(user.id)}.json")
			
	def Update(self, user: User, data):
		json.dump(data, open(f"{data_dir}tickets/{str(user.id)}.json", 'w'), indent=2)
	
	def Setup_Check(self, message):
		if f"{str(message.id)}.json" not in os.listdir(f"{data_dir}tickets/setup/"):
			return False
		else:
			return True
	
	def Setup_Load(self, message):
		return json.load(open(f"{data_dir}tickets/setup/{str(message.id)}.json", 'r'))
		
	def Setup_Delete(self, file):
		os.remove(f"{data_dir}tickets/setup/{file}")
		
	def Setup_Save(self, message, data):
		json.dump(data, open(f"{data_dir}tickets/setup/{str(message.id)}.json", 'w'), indent=2)