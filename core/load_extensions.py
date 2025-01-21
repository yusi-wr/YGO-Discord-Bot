from nextcord.ext import commands
from nextcord import Embed
from colorama import Fore, Back, Style
import os
from config import config

def embed(desc):
	embed = Embed(color=config["embed-color"])
	embed.description = f">>> **{desc}**"
	return embed

def load_extensions(bot: commands.Bot):
	
	#load the cogs files commands
	print(Fore.LIGHTCYAN_EX + " • Loading Cogs")
	for filename in os.listdir("./commands"):
		if filename.endswith("py") and filename != "__init__.py":
			bot.load_extension(f"commands.{filename[:-3]}")
			print(Fore.LIGHTMAGENTA_EX + f" • ({filename[:-3]})" + Fore.LIGHTGREEN_EX + " | Done")
			
	#load the cogs files events
	#print(Fore.LIGHTCYAN_EX + " • Loading Events •")
	for filename in os.listdir("./events"):
		if filename.endswith("py"):
			bot.load_extension(f"events.{filename[:-3]}")
			print(Fore.LIGHTMAGENTA_EX + f" • ({filename[:-3]})" + Fore.LIGHTGREEN_EX + " | Done")
	print(Fore.LIGHTYELLOW_EX + "-" * 20 + Style.RESET_ALL)


async def load_commands(ctx: commands.Context, bot: commands.Bot):
	
	try:
		for filename in os.listdir("./commands"):
			if filename.endswith("py") and filename != "__init__.py":
				bot.load_extension(f"commands.{filename[:-3]}")
		await ctx.reply(embed=embed(f"{config['emoji']['yes']} The command has been successfully restarted"))
	
	except AttributeError as Error:
		await ctx.reply(f"```{Error}```")


async def unload_commands(ctx: commands.Context, bot: commands.Bot):
	
	try:
		for filename in os.listdir("./commands"):
			if filename.endswith("py") and filename != "__init__.py":
				bot.unload_extension(f"commands.{filename[:-3]}")
		await ctx.reply(embed=embed(f"{config['emoji']['yes']} All commands have been successfully stopped"))
	
	except AttributeError as Error:
		await ctx.reply(f"```{Error}```")
		
async def reload_commands(ctx: commands.Context, bot: commands.Bot):
	
	try:
		for filename in os.listdir("./commands"):
			if filename.endswith("py") and filename != "__init__.py":
				bot.reload_extension(f"commands.{filename[:-3]}")
		await ctx.reply(embed=embed(f"{config['emoji']['yes']} All commands have been successfully reloaded"))
	
	except AttributeError as Error:
		await ctx.reply(f"```{Error}```")
	