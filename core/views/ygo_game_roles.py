from nextcord.ui import Button, button, View
from nextcord import Embed, Interaction, ButtonStyle
from config import config

emote = config["emoji"]
roles = config["game-role"]

def embed(desc):
	embed = Embed(color=config["embed-color"])
	embed.description = f">>> **{desc}**"
	embed.set_author(name=config["name"] + " | Game Roles")
	
	return embed


class ButtonGames(View):
	def __init__(self):
		super().__init__(timeout=None)
		
	@button(label="EDOPro", style=ButtonStyle.grey, emoji=emote["EDOPro"], custom_id="edopro")
	async def EDOPro(self, button: Button, interaction: Interaction):
		
		guild = interaction.guild
		user = interaction.user
		role = guild.get_role(roles["EDOPro"])
		
		if role:
			if role in user.roles:
				await user.remove_roles(role)
				reply = embed(desc=f"{emote['yes']} Role {role.mention} was successfully removed")
				await interaction.response.send_message(embed=reply, ephemeral=True)
			else:
				await user.add_roles(role)
				reply = embed(desc=f"{emote['yes']} Role {role.mention} added successfully")
				await interaction.response.send_message(embed=reply, ephemeral=True)
				
		else:
			reply = embed(desc=f"An error occurred and `EDOPro` could not be added")
			await interaction.response.send_message(embed=reply, ephemeral=True)
	
	@button(label="YGO Omega", style=ButtonStyle.grey, emoji=emote["YGOOmega"], custom_id="ygoomega")
	async def YGOOmega(self, button: Button, interaction: Interaction):
		
		guild = interaction.guild
		user = interaction.user
		role = guild.get_role(roles["YGOOmega"])
		
		if role:
			if role in user.roles:
				await user.remove_roles(role)
				reply = embed(desc=f"{emote['yes']} Role {role.mention} was successfully removed")
				await interaction.response.send_message(embed=reply, ephemeral=True)
			else:
				await user.add_roles(role)
				reply = embed(desc=f"{emote['yes']} Role {role.mention} added successfully")
				await interaction.response.send_message(embed=reply, ephemeral=True)
				
		else:
			reply = embed(desc=f"An error occurred and `YGOOmega` could not be added")
			await interaction.response.send_message(embed=reply, ephemeral=True)
	
	@button(label="Master duel", style=ButtonStyle.grey, emoji=emote["MasterDuel"], custom_id="masterduel")
	async def MasterDuel(self, button: Button, interaction: Interaction):
		
		guild = interaction.guild
		user = interaction.user
		role = guild.get_role(roles["MasterDuel"])
		
		if role:
			if role in user.roles:
				await user.remove_roles(role)
				reply = embed(desc=f"{emote['yes']} Role {role.mention} was successfully removed")
				await interaction.response.send_message(embed=reply, ephemeral=True)
			else:
				await user.add_roles(role)
				reply = embed(desc=f"{emote['yes']} Role {role.mention} added successfully")
				await interaction.response.send_message(embed=reply, ephemeral=True)
				
		else:
			reply = embed(desc=f"An error occurred and `MasterDuel` could not be added")
			await interaction.response.send_message(embed=reply, ephemeral=True)
		
	
	@button(label="DuelLinks", style=ButtonStyle.grey, emoji=emote["DuelLinks"], custom_id="duellinks")
	async def Duellinks(self, button: Button, interaction: Interaction):
		
		guild = interaction.guild
		user = interaction.user
		role = guild.get_role(roles["DuelLinks"])
		
		if role:
			if role in user.roles:
				await user.remove_roles(role)
				reply = embed(desc=f"{emote['yes']} Role {role.mention} was successfully removed")
				await interaction.response.send_message(embed=reply, ephemeral=True)
			else:
				await user.add_roles(role)
				reply = embed(desc=f"{emote['yes']} Role {role.mention} added successfully")
				await interaction.response.send_message(embed=reply, ephemeral=True)
				
		else:
			reply = embed(desc=f"An error occurred and `DuelLinks` could not be added")
			await interaction.response.send_message(embed=reply, ephemeral=True)
	
	
	@button(label="Dueling Nexus", style=ButtonStyle.grey, emoji=emote["Duelnexus"], custom_id="duelnexus")
	async def DuelNexus(self, button: Button, interaction: Interaction):
		
		guild = interaction.guild
		user = interaction.user
		role = guild.get_role(roles["Duelnexus"])
		
		if role:
			if role in user.roles:
				await user.remove_roles(role)
				reply = embed(desc=f"{emote['yes']} Role {role.mention} was successfully removed")
				await interaction.response.send_message(embed=reply, ephemeral=True)
			else:
				await user.add_roles(role)
				reply = embed(desc=f"{emote['yes']} Role {role.mention} added successfully")
				await interaction.response.send_message(embed=reply, ephemeral=True)
		else:
			reply = embed(desc=f"An error occurred and `Duelnexus` could not be added")
			await interaction.response.send_message(embed=reply, ephemeral=True)
	
	@button(label="Dueling Book", style=ButtonStyle.grey, emoji=emote["DuelBook"], custom_id="duelbook")
	async def Duelbook(self, button: Button, interaction: Interaction):
		
		guild = interaction.guild
		user = interaction.user
		role = guild.get_role(roles["DuelBook"])
		
		if role:
			if role in user.roles:
				await user.remove_roles(role)
				reply = embed(desc=f"{emote['yes']} Role {role.mention} was successfully removed")
				await interaction.response.send_message(embed=reply, ephemeral=True)
			else:
				await user.add_roles(role)
				reply = embed(desc=f"{emote['yes']} Role {role.mention} added successfully")
				await interaction.response.send_message(embed=reply, ephemeral=True)
				
		else:
			reply = embed(desc=f"An error occurred and `DuelBook` could not be added")
			await interaction.response.send_message(embed=reply, ephemeral=True)
	