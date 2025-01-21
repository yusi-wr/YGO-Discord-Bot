import nextcord
from nextcord import Embed
from nextcord import Interaction
from nextcord.ext import commands, application_checks
from config import config
from core import Functions


emote = config["emoji"]

def ErrorEmbed(desc):
	
	embed = Embed(color=config["embed-color"])
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1180266906314346677/1185547458160373820/Picsart_23-12-16_09-43-27-780.png")
	embed.title = f"**{emote['no']} Warning**"
	embed.description = f">>> **{desc}**"
	embed.set_author(name=config["name"], icon_url=config["icon"])
	
	return embed

class EventErreurs(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_application_command_error(self, interaction: Interaction, error: nextcord.ext.application_checks.errors):
	     guild = interaction.guild
	     
	     
	     if isinstance(error, application_checks.errors.ApplicationBotMissingPermissions):
	     	
	     	embed = ErrorEmbed(desc="I don't have the permissions for do this")
	     	return
	     	
	     else:
	     	embed = ErrorEmbed(desc=f"```{error}```")
	     	await interaction.response.send_message(embed=embed, ephemeral=True)
	
	
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		 	
		 if isinstance(error, commands.BotMissingPermissions):
		 	embed = ErrorEmbed(desc="I don't have the permissions for do this")
		 	await ctx.send(embed=embed)
		 	
		 elif isinstance(error, commands.MissingPermissions):
		 	embed = ErrorEmbed(desc="You don't' have the permissions for do this")
		 	await ctx.send(embed=embed)
		 	
		 else:
		 	embed = ErrorEmbed(desc=f"```{error}```")
		 	await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(EventErreurs(bot))