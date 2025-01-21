from nextcord import Interaction, Member, slash_command, TextChannel, SlashOption, Role, CategoryChannel, Attachment
from nextcord.ext import commands
from core import Functions, Slash_Command, TicketCommands


class Slash_commands(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.commands = Slash_Command(self.bot)
		self.functions = Functions(self.bot)
		self.tickets = TicketCommands(self.bot)
	
	
	#slash command set a backgrounds
	@slash_command(name="set-nickname", description="set a nicknale for your profile")
	async def SetNickname(self, interaction: Interaction,
	   nickname: str = SlashOption(name="nickname", description="new your name for set in your profile bot")
	):
		
		await self.commands.ChangeNickName(interaction=interaction, nickname=nickname)
		
	
	#slash command set a backgrounds
	@slash_command(name="set-background", description="set a bg for your profile")
	async def SetBackgrounds(self, interaction: Interaction,
	   AttachmentFile: Attachment = SlashOption(name="select-file", description="select image from your files", required=False),
	   BackgroundUrl: str = SlashOption(name="bg-url", description="paste here your image url", required=False),
	):
		
		await self.commands.ChangeBG(interaction=interaction, bg=AttachmentFile, img_url=BackgroundUrl)
	
	
	#slash command set a backgrounds
	@slash_command(name="set-profile", description="set a icon for your profile")
	async def SetProfileIcon(self, interaction: Interaction,
	   AttachmentFile: Attachment = SlashOption(name="select-file", description="select image from your files", required=False),
	   IconUrl: str = SlashOption(name="bg-url", description="paste here your image url", required=False),
	):
		
		await self.commands.ChangeProfile(interaction=interaction, bg=AttachmentFile, img_url=IconUrl)
	
	
	#slash command for admin`s send embed
	@slash_command(name="admin-message", description="for admins send message or news")
	async def AdminMessage(self, interaction: Interaction,
	   message: str = SlashOption(name="message", description="your message for send"),
	  channel: TextChannel = SlashOption(name="send-to", description="you channel for send this message", required=False),
	  is_for_new: str = SlashOption(name="message-for", choices=["news", "normal"], required=False, default="normal"),
	):
		
		if self.functions.CheckPermisions(interaction.user):
			await self.commands.AdminMessage(interaction=interaction, message=message, channel=channel, is_for_new=is_for_new)
		else:
			await self.functions.NonHasPermisions(interaction=interaction)
	
	
	#slash command for admin`s send embed
	@slash_command(name="admin-embed", description="for admins send embed msg or news")
	async def AdminEmbed(self, interaction: Interaction,
	   title: str = SlashOption(name="title", description="your embed title"),
	   desc: str = SlashOption(name="desc", description="your embed desc"),
	  img: Attachment = SlashOption(name="image", description="your image embed", required=False),
	  channel: TextChannel = SlashOption(name="send-to", description="you channel for send this embed", required=False),
	  is_for_new: str = SlashOption(name="embed-for", choices=["news", "normal"], required=False, default="normal"),
	):
		
		if self.functions.CheckPermisions(interaction.user):
			await self.commands.AdminEmbed(interaction=interaction, title=title, desc=desc, img=img, is_for_new=is_for_new, channel=channel)
		else:
			await self.functions.NonHasPermisions(interaction=interaction)
	
	#slash command setup tickets
	@slash_command(name="setup-ticket", description="Setup tickets and send to channel")
	async def SetupTicket(self, interaction: Interaction,
	   title: str = SlashOption(name="title", description="title for this ticket"),
	   desc: str = SlashOption(name="description", description="ticket description"),
	   channel: TextChannel = SlashOption(name="send-to", description="select channel ticket"),
	   category: CategoryChannel = SlashOption(name="category", description="select category to open ticket"),
	   is_free = SlashOption(name="its-free", description="the member need pay gems for open",choices=["yes", "no"], required=False, default="no")
	):
		
		if self.functions.CheckPermisions(interaction.user):
			await self.tickets.Setup(interaction=interaction, channel=channel, title=title, desc=desc, category=category, is_free=is_free)
		else:
			await self.functions.NonHasPermisions(interaction=interaction)
	
	#slash command clear setup tickets
	@slash_command(name="clear-setup-ticket", description="Clear all setup tickets")
	async def ClearSetup(self, interaction: Interaction):
		
		if self.functions.CheckPermisions(interaction.user):
			await self.tickets.ClearSetup(interaction=interaction)
		else:
			await self.functions.NonHasPermisions(interaction=interaction)
	
	#slash command clear setup tickets
	@slash_command(name="clear-ticket", description="Clear all tickets")
	async def ClearTickets(self, interaction: Interaction, reason: str = SlashOption(name="reason", required=False)):
		
		if self.functions.CheckPermisions(interaction.user):
			await self.tickets.ClearTickets(interaction=interaction, reason=reason)
		else:
			await self.functions.NonHasPermisions(interaction=interaction)
	
	#slash command for admin`s send embed
	@slash_command(name="role-games", description="for send button role of games to channel")
	async def GameButtonRole(self, interaction: Interaction,
	  channel: TextChannel = SlashOption(name="send-to", description="you channel for send this button")
	):
		
		if self.functions.CheckPermisions(interaction.user):
			await self.commands.RoleGameButtons(interaction=interaction, channel=channel)
		else:
			await self.functions.NonHasPermisions(interaction=interaction)
	
	
	#slash command settings
	@slash_command(name="settings", description="settings of the bot")
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def Settings(self, interaction: Interaction,
	    set_admin: Role = SlashOption(name="set-admin", description="set admin role for use commands admins", required=False),
	    remove_admin: Role = SlashOption(name="remove-admin", description="set admin role for use commands admins", required=False),
	    channel_log: TextChannel = SlashOption(name="chat-log", required=False),
	    bot_mention = SlashOption(name="bot-mention", required=False, choices={'here': '@here', 'everyone': '@everyone'}),
	    daliygift_channel: TextChannel = SlashOption(name="dailygift-channel", required=False),
	    welcome_role: Role = SlashOption(name="welcome-role", required=False),
	    cards_news: TextChannel = SlashOption(name="cards-news", required=False),
	    daily_gifts = SlashOption(name="daily-gifts", description="Enable/disable daily gifts", required=False, choices=["enable", "disable"])
	):
		
		await self.commands.Settings(interaction=interaction, channel_log=channel_log, bot_mention=bot_mention, set_admin=set_admin, remove_admin=remove_admin, daliygift_channel=daliygift_channel, welcome_role=welcome_role, cards_news=cards_news, daily_gifts=daily_gifts)
		
	
	
		

def setup(bot):
	bot.add_cog(Slash_commands(bot))