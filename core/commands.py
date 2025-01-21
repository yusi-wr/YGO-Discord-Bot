from nextcord import Member, User, Embed
from nextcord.ext import commands
from config import config
from core import Functions
from database import users, Load
import random
import datetime

emote_link = ["https://cdn.discordapp.com/emojis/824167043875995689.png", "https://cdn.discordapp.com/emojis/1158132855667445861.gif", "https://cdn.discordapp.com/emojis/1129485698278367272.png"]
context = commands.Context
emote = config["emoji"]


class CommandPointsSystem:
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.functions = Functions(self.bot)
		
	
	
	#------------------(commands functions)----------------
	
	async def BuyPoints(self, ctx: commands.Context, points = None):
		user = ctx.author
		data = users.Load(user)
		
		dict_list = {
		  "20": "18000",
		  "30": "35000",
		  "40": "44000",
		  "50": "57000",
		  "60": "62100",
		  "70": "73000",
		  "80": "81400",
		  "90": "92000",
		  "120": "125000",
		  "205": "210500",
		  "300": "340000",
		  "400": "420000",
		  "500": "560000",
		  "1000": "1000000"
		}
		def get_show_list(title):
			text = ""
			for point in dict_list:
				text += f"- {emote['points']} {int(point):,} = {emote['gems']} {int(dict_list[point]):,}\n"
			embed = self.functions.embed(desc=f"{text}", title=f"**{title}**")
			
			return embed
		
		if points == None:
			reply = get_show_list("List of points. To buy `?buy-points`")
			await ctx.reply(embed=reply)
			return
			
		if points not in dict_list:
			reply = get_show_list(f"{emote['no']} You must select points in this list") 
			await ctx.reply(embed=reply)
			return
		elif data["gems"] < int(dict_list[points]):
			reply = get_show_list(f"{emote['no']} Sorry, you don't have enough to buy the required points\nYour gems: {emote['gems']} {data['gems']:,}")
			await ctx.reply(embed=reply)
			return
		
		the_points = int(points) + random.randint(2, 5)
		price = int(dict_list[points])
		data["gems"] -= price
		data["dp"] += the_points
		users.Update(user, data)
		
		embed = self.functions.embed(desc=f"Purchase completed successfully\n- Points received: {emote['points']} {the_points:,}\nPrice: {emote['gems']} {price:,}")
		await ctx.reply(embed=embed)
	
	
	async def AddGemsToUser(self, ctx: context, user: Member, Gems: int):
		
		author = ctx.author
		settings= Load("settings.json")
		
		if user and not self.functions.Check_in_guild(user, ctx.guild):
			await self.functions.ErrorPrefix(errorLog="People outside the server have their accounts blocked. Sorry, the user must be back on the server", ctx=ctx)
			return
		
		elif Gems <= 0:
			await self.functions.ErrorPrefix(errorLog="There must not be an actual value to add", ctx=ctx)
			await ctx.send(random.choice(emote_link))
			return 
		
		elif Gems > 25000:
			await self.functions.ErrorPrefix(errorLog=f"Maximum add Gems: {emote['gems']} 25,000", ctx=ctx)
			return
		elif user.id == author.id and author.id not in settings["owners"]:
			await self.functions.ErrorPrefix(errorLog="You cannot add points to yourself", ctx=ctx)
			return
		
		data = users.Load(user)
		data["gems"] += Gems
		users.Update(user, data)
		
		embed = self.functions.embed(
		    desc=f"New `Gems` added to {user.mention} successfully\n- By: {author.mention}\n`-------------`\n- Add: {emote['gems']} {Gems:,}\n- Has now: {emote['gems']} {data['gems']:,}",
		    title="Add Gems to player`s",
		    icon=config["img"]["done"]
		)
		
		await ctx.reply(f"• {user.mention} •",embed=embed)
	
	
	async def AddDPToUser(self, ctx: context, user: Member, DP: int):
		
		author = ctx.author
		settings= Load("settings.json")
		
		if user and not self.functions.Check_in_guild(user, ctx.guild):
			await self.functions.ErrorPrefix(errorLog="People outside the server have their accounts blocked. Sorry, the user must be back on the server", ctx=ctx)
			return
		
		elif DP <= 0:
			await self.functions.ErrorPrefix(errorLog="There must not be an actual value to add", ctx=ctx)
			await ctx.send(random.choice(emote_link))
			return 
		
		elif DP > 50:
			await self.functions.ErrorPrefix(errorLog=f"Maximum add DP: {emote['points']} 50", ctx=ctx)
			return
		elif user.id == author.id and author.id not in settings["owners"]:
			await self.functions.ErrorPrefix(errorLog="You cannot add points to yourself", ctx=ctx)
			return
		
		data = users.Load(user)
		data["dp"] += DP
		users.Update(user, data)
		
		embed = self.functions.embed(
		    desc=f"New `DP` points added to {user.mention} successfully\n- By: {author.mention}\n`-------------`\n- Add: {emote['points']} {DP}\n- Has now: {emote['points']} {data['dp']}",
		    title="Add DP Points",
		    icon=config["img"]["done"]
		)
		
		await ctx.reply(f"• {user.mention} •",embed=embed)
	
	
	#function command daily 
	async def Daily(self, ctx: context):
		
		user = ctx.author
		data = users.Load(user)
		
		if self.functions.check_cooldwon(user=user, command="daily"):
			dailyGem = random.randint(1500, 3000)
			dailyDP = random.randint(1, 5)
			
			data["dp"] += dailyDP
			data["gems"] += dailyGem
			users.Update(user=user, data=data)
			
			embed = self.functions.embed(
			   title="**Daily Gifts**",
			   desc=f"You have successfully received the gift\n`-----------`\nGems: {emote['gems']} {dailyGem}\nDP: {emote['points']} {dailyDP}\nThank ^_^",
			   icon="https://cdn.discordapp.com/emojis/835271803743371314.png"
			)
			
			await ctx.reply(embed=embed)
		else:
			time = self.functions.get_cooldwon(user=user, command="daily")
			embed = self.functions.embed(
			    desc=f"You have already claimed and received your daily points\n\n{emote['time']} Time left: {time}",
			    icon="https://cdn.discordapp.com/emojis/1040304103559004191.png"
			)
			
			await ctx.reply(embed=embed)
	
	
	#function command transfer gems from users
	async def Transfer(self, ctx: context, user: Member, gem: int):
		
		if user and not self.functions.Check_in_guild(user, ctx.guild):
			await self.functions.ErrorPrefix(errorLog="People outside the server have their accounts blocked. Sorry, the user must be back on the server", ctx=ctx)
			return
		
		author = ctx.author
		authorData = users.Load(author)
		userData = users.Load(user)
		
		if authorData["gems"] < gem:
			await self.functions.ErrorPrefix(errorLog=f"Excuse you don't have enough to transfer to {user.mention}\nYour account: {emote['gems']} {authorData['gems']:,}", ctx=ctx)
			return
		elif gem <= 0:
			await ctx.reply(random.choice(emote_link))
			return
		elif user.id == author.id:
			await ctx.reply(random.choice(["https://cdn.discordapp.com/emojis/780144096467222538.png", "https://cdn.discordapp.com/emojis/872280226963521568.png"]))
			return
		
		authorData["gems"] -= gem
		userData["gems"] += gem
		
		users.Update(user, userData); users.Update(author, authorData)
		
		await ctx.reply(
		embed=self.functions.embed(
		desc=f"The gems have been converted by you to {user.mention}.\nConversion: {emote['gems']} {gem:,}",
		icon=config["img"]["done"],
		title="**Transfer gem`s**"
		)
		)
		
		try:
			await user.send(f"**Hello Mr. {user.mention}**",embed=self.functions.embed(desc=f"**Sorry for the inconvenience/nYou have received a conversion: {emote['gems']} {gem:,}\nfrom {author.mention}**", icon="https://cdn.discordapp.com/emojis/1079031910010978315.png"))
		except:
			return None
		
	
	#function command show profile
	async def ProfileUser(self, ctx: context, user: Member=None):
		
		if user and not self.functions.Check_in_guild(user, ctx.guild):
			await self.functions.ErrorPrefix(errorLog="Sorry, no user information can be displayed outside the server. The user's account is frozen", ctx=ctx)
			return
		if user == None:
			user= ctx.author
		
		data = users.Load(user)
		
		nick = data["nickname"]
		gems = data["gems"]
		db = data["dp"]
		cup = data["cup"]
		bg = data["bg"]
		icon = data["icon"]
		Duel_count = data["duels"]["count"]
		Duel_win = data["duels"]["win"]
		Duel_lose = data["duels"]["lose"]
		rank = self.functions.RankCall(db)
		
		embed = Embed(color=config["embed-color"])
		embed.title = f"{emote['star']} **{nick}** {emote['star']}" if nick != None else f"• **{user.display_name} •**"
		embed.description = f">>> **Gems: {emote['gems']} {gems:,}\nDP: {emote['points']} {db:,}\nCup: {emote['cup-winner']} {cup}\nRank: {rank}**"
		embed.add_field(name=f"{emote['duel']} **Duels: {Duel_count}**", value=f">>> **- Win: {Duel_win}\n- Lose: {Duel_lose}**")
		
		embed.set_author(name=config["name"] + " | Duelists", icon_url=config["icon"])
		embed.set_thumbnail(url=icon if icon else user.avatar.url)
		embed.set_image(url=bg if bg else config["img"]["bg"])
		
		await ctx.reply(embed=embed)
		
	#uptime command function
	async def Uptime(self, ctx: context, start_time):
		def convert_timedelta(duration):
			days, seconds = divmod(duration.total_seconds(), 86400)
			hours, seconds = divmod(seconds, 3600)
			minutes, seconds = divmod(seconds, 60)
			return int(days), int(hours), int(minutes), int(seconds)
		
		current_time = datetime.datetime.utcnow()
		uptime_duration = current_time - start_time
		days, hours, minutes, seconds = convert_timedelta(uptime_duration)
		
		embed = self.functions.embed(
		   desc=f"- {days}D {hours}H {minutes}M {seconds}S",
		   title=f"{self.bot.user.display_name} • Uptime",
		   icon="https://cdn.discordapp.com/emojis/945256100935139338.png"
		   )
		
		await ctx.reply(embed=embed)
	
	
	#bot ping
	async def ping(self, ctx: context):
		
		latency = round(self.bot.latency * 1000)
		embed = self.functions.embed(
		   desc=f"- {emote['latency']} Latency: {latency}ms",
		   title=f"{self.bot.user.display_name} • Latency",
		   icon=self.bot.user.avatar.url
		)
		
		await ctx.reply(embed=embed)