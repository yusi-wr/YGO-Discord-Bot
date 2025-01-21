from nextcord import Interaction, ButtonStyle, Embed, utils, PermissionOverwrite
from nextcord.ui import View, TextInput, button, Button, Modal
from nextcord.ext import commands
from database import tickets, users, Load
from config import config, loading
from .embeds import *
from .functions import TicketFunction
from datetime import datetime, timedelta
from random import randint, choice

emote = config["emoji"]

def check_date(ticket_date):
	
	date = datetime.strptime(ticket_date, "%Y-%m-%d %H:%M:%S.%f")
	diff = datetime.utcnow() - date
			
	if (diff.total_seconds() / 3600) >= 24:
		return True
	else:
		return False

class ViewTickets(View):
	def __init__(self, bot: commands.Bot):
		super().__init__(timeout=None)
		self.bot = bot
		
	
	#button open tickets
	@button(label="Create ticket", style=ButtonStyle.gray, emoji=emote["ticket"], custom_id="openticket")
	async def OpenTickets(self, button: Button, interaction: Interaction):
		
		msg = await interaction.response.send_message(embed=loading, ephemeral=True)
		
		message = interaction.message
		user = interaction.user
		guild = interaction.guild
		
		if not tickets.Setup_Check(message):
			await msg.edit(embed=embed_reply("This ticket is no longer available for use, sorry 😔\nThe admin should \n- use: `/setup-ticket` for create new one or use\n- use: `/update-setup-ticket` for update this ticket"))
			return
		
		settings = Load("settings.json")
		ticketData = tickets.Setup_Load(message)
		userData = users.Load(user)
		is_free = ticketData["is_free"]
		
		if tickets.check(user):
			userTicket = tickets.Load(user)
			channel = await self.bot.fetch_channel(userTicket["channel"])
			await msg.edit(embed=embed_reply(f"Sorry, you already have a ticket\n- Your ticket: {channel.mention}\nYou cannot open another ticket if the old one has not been deleted"))
			return
		
		if is_free != "yes":
			if userData["gems"] < 1200:
				await msg.edit(embed=Embed(color=config["embed-color"], description=f">>> **Sorry, but this ticket is paid. You need to pay {emote['gems']}{1200:,} to open a ticket**"))
				return
			else:
				userData["gems"] -= 1200
				users.Update(user=user, data=userData)
		
		category = utils.get(guild.categories, id=ticketData["category"])
		admins = [guild.get_role(role) for role in settings["admins"]]
		if not category:
			overwrite = overwrite = {
			guild.default_role: PermissionOverwrite(view_channel=False)
			}
			category = await guild.create_category(name="Tickets", overwrites=overwrite)
			
		overwrite = overwrite = {
	        guild.default_role: PermissionOverwrite(view_channel=False),
	        user: PermissionOverwrite(view_channel=True),
	        }
		
		if len(admins) >= 1:
			for admin in admins:
				overwrite[admin] = PermissionOverwrite(view_channel=True)
		
		channel = await guild.create_text_channel(name=f"🎟│{user.name}️", category=category, overwrites=overwrite)
		
		mention = f"@here | {user.mention}" + " | ".join(role.mention for role in admins) if len(admins) >= 1 else f" @here | {user.mention}"
		message_settings = await channel.send(mention, embed=embed_tickets(user=user, is_free=is_free), view=ViewSettingsTicket(user=user, bot=self.bot))
		
		data = {}
		data["channel"] = channel.id
		data["msg"]= message_settings.id
		data["is_free"] = is_free
		data["date"] = str(datetime.utcnow())
		tickets.Update(user, data)
		
		await msg.edit(embed=Embed(color=config["embed-color"], description=f"The ticket was created successfully\n- Your ticket {channel.mention}"))

	
class ViewSettingsTicket(View):
	def __init__(self, user: User, bot: commands.Bot):
		super().__init__(timeout=None)
		
		self.bot = bot
		self.author = user
		self.functions = TicketFunction(self.bot)
	
	#button add user in ticket
	@button(label="Add", style=ButtonStyle.green, emoji=emote["join"])
	async def AddUser(self, button: Button, interaction: Interaction):
		
		
		user = interaction.user
		guild = interaction.guild
		
		if not self.functions.CheckPermisions(user) and user.id != self.author.id:
			await interaction.response.send_message(embed=embed_reply("Sorry, you do not have permission for add user in this ticket"))
			return
			
		await interaction.response.send_modal(AddUser(channel=interaction.channel))
	
	#button add user in ticket
	@button(label="Remove", style=ButtonStyle.red, emoji=emote["leave"])
	async def RemoveUser(self, button: Button, interaction: Interaction):
		
		user = interaction.user
		guild = interaction.guild
		
		if not self.functions.CheckPermisions(user) and user.id != self.author.id:
			await interaction.response.send_message(embed=embed_reply("Sorry, you do not have permission for add user in this ticket"))
			return
			
		await interaction.response.send_modal(RemoveUser(channel=interaction.channel))
		
	
	#button close ticket
	@button(label="Close", style=ButtonStyle.red, emoji=emote["close"])
	async def CloseTicket(self, button: Button, interaction: Interaction):
		
		msg = await interaction.response.send_message(embed=loading, ephemeral=True)
		user = interaction.user
		guild = interaction.guild
		settings = Load("settings.json")
		data = tickets.Load(self.author)
		userData = users.Load(self.author)
		
		if not self.functions.CheckPermisions(user) and user.id != self.author.id:
			await msg.edit(embed=embed_reply("Sorry, you do not have permission to delete the ticket"))
			return
			
		await interaction.channel.delete()
		tickets.Delete(self.author)
		
		if user.id != self.author.id:
			if not check_date(data["date"]) and data["is_free"] != "yes":
				compensation = randint(400, 500)
				userData["gems"] += compensation
				users.Update(self.author, userData)
				comp_text = f"You will be compensated a small amount if the ticket is deleted 24 hours before it is opened\n- Compensation: {emote['gems']} {compensation}"
			else:
				comp_text = ""
				
			embed_to_user = embed_reply(desc=f"Hello {self.author.mention}\nYour ticket has been closed/deleted by {user.mention}{comp_text}")
			
			try:
				await self.author.send(embed=embed_to_user)
			except:
				pass
		else:
			pass
			
			

#class model for add user`s in tickets
class AddUser(Modal):
	def __init__(self, channel):
		super().__init__(title="Add a user to a ticket", timeout=None)
		
		self.channel = channel
		
		self.user = TextInput(
		     label="User ID",
		     min_length=9,
		     max_length=22,
		     required=True,
		     placeholder="Add one user ID you add to here"
		)
		self.add_item(self.user)
	
	async def callback(self, interaction: Interaction) -> None:
		user = interaction.guild.get_member(int(self.user.value))
		
		
		if user is None:
			embed = embed_reply("Please provide the required user ID")
			await interaction.response.send_message(embed=embed)
			return
		
		overwrite = PermissionOverwrite()
		overwrite.view_channel = True
		overwrite.read_messages = True
		
		await self.channel.set_permissions(user, overwrite=overwrite)
		embed = embed_reply(f"You have been added to this ticket\n- By: {interaction.user.mention}")
		
		await interaction.channel.send(f"{user.mention}", embed=embed)
		await interaction.response.send_message(embed=embed_reply("User added successfully"), ephemeral=True)


#class model for remove user`s from tickets
class RemoveUser(Modal):
	def __init__(self, channel):
		super().__init__(title="Remove a user to a ticket", timeout=None)
		
		self.channel = channel
		
		self.user = TextInput(
		     label="User ID",
		     min_length=9,
		     max_length=22,
		     required=True,
		     placeholder="Add one user ID you want to remove"
		)
		self.add_item(self.user)
	
	async def callback(self, interaction: Interaction) -> None:
		user = interaction.guild.get_member(int(self.user.value))
		
		
		if user is None:
			embed = embed_reply("Please provide the required user ID")
			await interaction.response.send_message(embed=embed)
			return
		
		overwrite = PermissionOverwrite()
		overwrite.view_channel = False
		overwrite.read_messages = False
		
		await self.channel.set_permissions(user, overwrite=overwrite)
		
		await interaction.response.send_message(embed=embed_reply("User removed successfully"), ephemeral=True)