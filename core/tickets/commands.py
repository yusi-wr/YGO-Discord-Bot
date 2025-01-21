from nextcord import Embed, Interaction, TextChannel, CategoryChannel
from nextcord.ext import commands
from .embeds import *
from database import Update, Load
from config import config, loading
from core import Functions
from .functions import TicketFunction
from .views import ViewTickets

emote = config["emoji"]

class TicketCommands:
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.functions = Functions(self.bot)
		self.functions_ticket = TicketFunction(self.bot)
	
	
	#function setup tickets
	async def Setup(self, interaction: Interaction, title: str, desc: str, channel: TextChannel, category: CategoryChannel, is_free="no"):
		
		msg_response = await interaction.response.send_message(embed=loading)
		settings = Load("settings.json")
		
		guild = interaction.guild
		embed = embed_setup(desc=desc, title=title, is_free=is_free)
		
		await self.functions.Send_line_Image(channel, "ticket.png")
		message = await channel.send(f"• {settings['bot-mention']} •", embed=embed, view=ViewTickets(self.bot))
		await self.functions.Send_line_Image(channel, "line.png")
		
		await self.functions_ticket.setup(message=message, category=category, channel=channel, is_free=is_free)
		
		embed_reply = self.functions.embed(desc=f"Ticket system installed successfully \n- Channel: {channel.mention}")
		
		await msg_response.edit(embed=embed_reply)
	
	
	#clear setup tickets
	async def ClearSetup(self, interaction: Interaction):
		
		try:
			msg_response = await interaction.response.send_message(embed=loading)
			await self.functions_ticket.claer_setup()
			await msg_response.edit(embed=self.functions.embed(desc=f"{emote['yes']} All setup tickets have been successfully deleted"))
		except AttributeError as Error:
			await self.functions.ErrorSlash(errorLog=f"```{Error}```", interaction=interaction)
			
	async def ClearTickets(self, interaction: Interaction, reason="None..."):
		
		try:
			msg_response = await interaction.response.send_message(embed=loading)
			
			result = await self.functions_ticket.clear_tickets(reason=reason)
			if result is not None:
				embed = embed_reply(desc=f"{emote['yes']} Successfully completed\n- Delete {result} tickets")
			else:
				embed = embed_reply(desc=f"An error occurred unless any ticket was deleted")
			await msg_response.edit(embed=embed)
		except AttributeError as Error:
			await self.functions.ErrorSlash(errorLog=f"```{Error}```", interaction=interaction)
		
		
		
		
		
		