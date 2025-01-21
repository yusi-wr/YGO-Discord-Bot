from nextcord.ui import Button, View, button
from nextcord import Member, TextChannel, ButtonStyle, Interaction, Embed, Role, Message, User
from nextcord.ext import commands
from database import tournaments, Load
from config import config
from .embeds import embed_tounaments, embed_log

emote = config["emoji"]

#buttons
class ClassButtonTournament(View):
	def __init__(self, Manager: Member, name: str,chat_announce: TextChannel, bot: commands.Bot, role: Role):
		super().__init__(timeout=None)
		
		self.name = name
		self.bot = bot
		self.manager = Manager
		self.data = tournaments
		self.settings = Load(file="settings.json")
		self.channel_announce = chat_announce
		self.role = role
	
	@button(label="Join", style=ButtonStyle.green, emoji=emote["join"])
	async def JoinTournaments(self, button: Button, interaction: Interaction):
		
		data = self.data.Load(self.manager)
		user = interaction.user
		
		if user.id in data["participants"]:
			view = View()
			view.add_item(ButtonLeave(manager=self.manager, role=self.role))
			await interaction.response.send_message("**You are already participating in the tournament 😅**",ephemeral=True, view=view)
			
		else:
			data["participants"].append(user.id)
			await user.add_roles(self.role)
			self.data.Update(self.manager, data)
			await interaction.response.send_message(f"**Registered in the list of tournament participants**", ephemeral=True)
			
	
	@button(label="Participants", style=ButtonStyle.gray, emoji=emote["list"])
	async def ParticipantsShow(self, button: Button, interaction: Interaction):
		
		embed = Embed(description=f"**{emote['loading']} Loading...**")
		msg = await interaction.send(embed=embed, ephemeral=True)
		data = self.data.Load(self.manager)
		participants = data["participants"]
		
		text = ""
		who_leave = ""
		count = 0
		for user_id in participants:
			count += 1
			user = await self.bot.fetch_user(user_id)
			
			if user not in interaction.guild.members:
				who_leave += f"- {user.mention}\n"
			text += f"{emote['number'][count] if count in emote['number'] else count} | {user.mention}\n"
		
		embed: Embed = embed_tounaments(name=self.name, desc=text, manager=self.manager)
		embed.set_image(url=config["img"]["tournament"])
		if who_leave != "":
			embed.add_field(name=f"**{emote['leave']} Lift from server**", value=f">>> **{who_leave}**")
		
		await msg.edit(embed=embed)


class ButtonLeave(Button):
	def __init__(self, manager: Member, role: Role):
		super().__init__(label="Leave", style=ButtonStyle.red, emoji=emote["leave"])
		
		self.manager = manager
		self.role = role
	async def callback(self, interaction: Interaction):
		
		data = tournaments.Load(self.manager)
		user = interaction.user
		
		participants = data["participants"]
		
		if user.id in participants:
			data["participants"].remove(user.id)
			tournaments.Update(user=self.manager, data=data)
			await user.remove_roles(self.role)
			await interaction.response.send_message("**You have been logged out of the tournament. Thank you**", ephemeral=True)
		else:
			await interaction.response.send_message("**Sorry, you are not registered for the tournament**", ephemeral=True)
		

class ClassViewLog_Info(View):
	def __init__(self, manager: Member, bot: commands.Bot):
		super().__init__(timeout=None)
		self.manager = manager
		self.bot = bot
		self.tourna_data = tournaments
	
	@button(label="Stats", style=ButtonStyle.gray, emoji=emote["stats"])
	async def Stats(self, button: Button, interaction: Interaction):
		
		embed = Embed(description=f"**{emote['loading']} Loading...**")
		msg = await interaction.response.send_message(embed=embed, ephemeral=True)
		
		data = self.tourna_data.Load(self.manager)
		current_round = [await self.bot.fetch_user(x) for x in data["current-round"]]
		next_round = [await self.bot.fetch_user(x) for x in data["next-round"]]
		leave = [await self.bot.fetch_user(x) for x in data["leave"]]
		
		current_round_list = "\n".join(u.mention for u in current_round) if len(current_round) != 0 else "- **0**"
		next_round_list = "\n".join(u.mention for u in next_round) if len(next_round) != 0 else "- **0**"
		Out_of_competition = "\n".join([x.mention for x in leave]) if len(leave) != 0 else "- **0**"
		
		embed = Embed(color=config["embed-color"])
		embed.title = f"• {data['name']} •"
		embed.description = f">>> **View statistics for the current round in the tournament\n- {emote['round']} Current round: {data['round']} **"
		embed.add_field(name=f"** {emote['round']} In the field**", value=f">>> {current_round_list}")
		embed.add_field(name=f"** {emote['yes']} Round candidates: {data['round'] + 1 if data['round'] != 'final' else 'final'}**", value=f">>> {next_round_list}")
		embed.add_field(name=f"** {emote['no']} Out of competition**", value=f">>> {Out_of_competition}")
		embed.set_image(url=config["img"]["tournament"])
		
		await msg.edit(embed=embed)
	
	
	@button(label="Match`s", style=ButtonStyle.gray, emoji=emote["round"])
	async def Round_Log(self, button: Button, interaction: Interaction):
		
		embed = Embed(description=f"**{emote['loading']} Loading...**")
		msg = await interaction.response.send_message(embed=embed, ephemeral=True)
		
		
		embed = embed_log(self.manager)
		
		await msg.edit(embed=embed)
	
	
	@button(label="Logs", style=ButtonStyle.gray, emoji=emote["log"])
	async def TournaLog(self, button: Button, interaction: Interaction):
		embed = Embed(description=f"**{emote['loading']} Loading...**")
		msg = await interaction.response.send_message(embed=embed, ephemeral=True)
		
		data = tournaments.Load(self.manager)
		
		embed = Embed(color=config["embed-color"])
		embed.description = f">>> ** - {emote['log']} Match Logs**"
		embed.title = f"**{data['name']}**"
		if len([x for x in data["log"]]) >= 1:
			for key in data["log"]:
				list_log = data["log"][key]
				text = ""
				for log in list_log:
					text += f"{log}\n"
					
				embed.add_field(name=f"**{emote['round']} Round: {key}**", value=f">>> **{text}**")
		else:
			embed.add_field(name=f"**{emote['round']} Log round {data['round']}**", value=f">>> - **Non any round log save....**")
		
		embed.set_author(name=config["name"] + " | Tournaments", icon_url=config["icon"])
		embed.set_image(url=config["img"]["tournament"])
		
		await msg.edit(embed=embed)



class ConfirmQualify(View):
	def __init__(self, manager: Member, player: User, msg: Message):
		super().__init__(timeout=60)
		
		self.message = msg
		self.player = player
		self.manager = manager
	
	async def on_timeout(self):
		for button in self.children:
			button.disabled=True
		await self.message.edit(view=self)
		
	
	@button(label="Yes", style=ButtonStyle.green, emoji=emote["yes"])
	async def Yes(self, button: Button, interaction: Interaction):
		
		data = tournaments.Load(self.manager)
		embed = Embed(color=config["embed-color"])
		if self.player.id in data["current-round"]:
			data["current-round"].remove(self.player.id)
			data["next-round"].append(self.player.id)
			
			embed.description = f"**Congratulations to you for qualifying for the `{data['round']}` round of the tournament\n- {emote['cup']} Tournament: `{data['name']}`\n- {emote['manager']} Organizer: {self.manager.mention}**"
			
			reply = "**The player has successfully qualified for the next round\nExclude his opponent using: ?t-exclude**"
			
		else:
			data["leave"].remove(self.player.id)
			data["next-round"].append(self.player.id)
			
			embed.description = f"**You have been disqualified and are no longer eligible for the next round\n- {emote['cup']} Tournament: `{data['name']}`\n- {emote['manager']} Organizer: {self.manager.mention}**"
			
			reply = "**The player has successfully qualified for the next round**"
			
		tournaments.Update(self.manager, data)
		
		
		await interaction.channel.send(f"{self.player.mention}", embed=embed)
		
		await self.on_timeout()
		
		await interaction.response.send_message(reply, ephemeral=True)
	
	
	@button(label="Cancel", style=ButtonStyle.red, emoji=emote["no"])
	async def Cancel(self, button: Button, interaction: Interaction):
		
		await self.on_timeout()


class ConfirmExclude(View):
	def __init__(self, manager: Member, player: User, msg: Message):
		super().__init__(timeout=60)
		
		self.message = msg
		self.player = player
		self.manager = manager
	
	async def on_timeout(self):
		for button in self.children:
			button.disabled=True
		await self.message.edit(view=self)
		
	
	@button(label="Yes", style=ButtonStyle.green, emoji=emote["yes"])
	async def Yes(self, button: Button, interaction: Interaction):
		
		data = tournaments.Load(self.manager)
		embed = Embed(color=config["embed-color"])
		if self.player.id in data["current-round"]:
			data["current-round"].remove(self.player.id)
			data["leave"].append(self.player.id)
			
			embed.description = f"**You have been excluded from the round `{data['round']}`\n- {emote['cup']} Tournament: `{data['name']}`\n- {emote['manager']} Organizer: {self.manager.mention}**"
			
		else:
			data["next-round"].remove(self.player.id)
			data["leave"].append(self.player.id)
			
			embed.description = f"**You have been disqualified and are no longer eligible for the next round\n- {emote['cup']} Tournament: `{data['name']}`\n- {emote['manager']} Organizer: {self.manager.mention}**"
			
		tournaments.Update(self.manager, data)
		
		await interaction.channel.send(f"{self.player.mention}", embed=embed)
		
		await self.on_timeout()
		
		await interaction.response.send_message("**The player has successfully qualified for the next round**", ephemeral=True)
	
	@button(label="Cancel", style=ButtonStyle.red, emoji=emote["no"])
	async def Cancel(self, button: Button, interaction: Interaction):
		
		await self.on_timeout()