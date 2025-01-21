from nextcord import Interaction, Embed, Member
from nextcord.ext import commands
from config import config
from database import challenges, users, data_dir
from .functions import FunctionsHelp
from .views import ChallengeConfirm
from core import Functions
from .embeds import *
from random import randint
import os
from core.views import Pages

emote = config["emoji"]
context = commands.Context

class CommandDuelSystem:
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.challenge_functions = FunctionsHelp(self.bot)
		self.functions = Functions(self.bot)
	
	
	
	#show challenges
	async def ShowChallenges(self, ctx: context, player: Member=None):
		
		author = ctx.author
		
		if player is not None:
			if not challenges.check(player):
				if player.id == ctx.author.id:
					await self.functions.ErrorPrefix(errorLog=f"No challenge created by you was found", ctx=ctx)
				else:
					await self.functions.ErrorPrefix(errorLog=f"No challenge created by {player.mention} was found.", ctx=ctx)
				return
			
			data = challenges.Load(player=player)
			opponent = await self.bot.fetch_user(data['opponent'])
			points = data["points"]
			
			embed = embed_challenge_show(player=player, opponent=opponent, points=points)
			
			await ctx.reply(embed=embed)
			
		else:
			embeds = []
			for file in os.listdir(f"{data_dir}challenges/"):
				if file == "challenges.txt":
					continue 
				player = await self.bot.fetch_user(int(file[:-5]))
				data = challenges.Load(player)
				
				opponent = await self.bot.fetch_user(data['opponent'])
				points = data["points"]
				embed = embed_challenge_show(player=player, opponent=opponent, points=points)
				
				embeds.append(embed)
				
			if len(embeds) > 1:
				embed: Embed = embeds[0]
				embed.set_footer(text=f"📑 Page: 1/{len(embeds)} | By: {author.name}")
				msg = await ctx.reply(embed=embed)
				await msg.edit(view=Pages(msg=msg, embeds=embeds, auther=author))
			elif len(embeds) == 1:
				await ctx.reply(embed=embeds[0])
			else:
				embed = self.functions.embed(
				  desc="No challenges found",
				  icon=author.avatar.url
				)
				await ctx.reply(embed=embed)
	
	
	#delete challenges 
	async def DeleteChallenge(self,ctx: context, player: Member=None):
		
		if player is None:
			player = ctx.author
		
		if not challenges.check(player):
			if player.id == ctx.author.id:
				await self.functions.ErrorPrefix(errorLog=f"No challenge created by you was found", ctx=ctx)
			else:
				await self.functions.ErrorPrefix(errorLog=f"No challenge created by {player.mention} was found.", ctx=ctx)
			return
			
		data = challenges.Load(player)
		points = data["points"]
		opponent = await self.bot.fetch_user(data["opponent"])
		createdBy = data["by"]
		
		if not self.functions.CheckPermisions(ctx.author) and ctx.author.id != createdBy:
			await self.functions.ErrorPrefix(errorLog=f"The challenge can only be deleted by the admin or the person created the challenge", ctx=ctx)
			return
		
		embed = embed_challenge_delete(player=player, opponent=opponent, points=points, author=ctx.author)
		
		challenges.Delete(player)
		
		reply = f">>> **The challenge has been deleted ✓\n{player.mention} {emote['vs']} {opponent.mention}**"
		await ctx.reply(reply, embed=embed)
	
	#remove one duel lose from profile
	async def RemoveLose(self, ctx: context):
		
		Member = ctx.author
		data = users.Load(Member)
		price = 4500
		if self.functions.check_cooldwon(user=Member, command="remove-lose"):
			if data["duels"]["lose"] <= 0:
				reply = embed_reply(desc="No recorded loss was found")
				await ctx.reply(embed=reply)
				return
			elif data["gems"] < price:
				reply = embed_reply(desc=f"Sorry, you do not have enough gems to perform the operation\n- You have: {emote['gems']} {data['gems']:,}\n- You need: {emote['gems']} {price:,}")
				await ctx.reply(embed=reply)
				return
			
			data["duels"]["lose"] -= 1
			data["duels"]["count"] -= 1
			data["gems"] -= price
			users.Update(Member, data)
			
			reply = embed_reply(desc=f"One recorded loss has been successfully removed\n- The rest: {data['duels']['lose']}\n- Payment: {emote['gems']} {price:,}")
			
			await ctx.reply(embed=reply)
		else:
			time = self.functions.get_cooldwon(user=Member, command="remove-lose")
			embed = self.functions.embed(
			    desc=f"You must wait for the time to expire to reuse this command\n\n{emote['time']} Time left: {time}",
			    icon="https://cdn.discordapp.com/emojis/1040304103559004191.png"
			)
			await ctx.reply(embed=embed)
	
	
	#delete one duel history`s
	async def DeleteHistory(self, ctx: context, date):
		
		date = str(date)
		player = ctx.author
		plaerData = users.Load(player)
		duelData = users.Duels_Data(player)
		
		if date not in duelData["duels"]:
			await self.functions.ErrorPrefix(errorLog=f"You must write the date correctly\nFor example: `?delete-history 2024/06/03 14:37:11`", ctx=ctx)
			return
			
		price = 1200
		if plaerData["gems"] < price:
			await self.functions.ErrorPrefix(errorLog=f"You need to pay {emote['gems']}{price:,} gem to delete duel history", ctx=ctx)
			return
		
		plaerData["gems"] -= price
		
		duelhistory = duelData["duels"][date]
		embed = self.functions.embed(
		   desc=f"**Delete duel date\n- {emote['date']} Date: {date}\n{emote['score']} Match score\n{duelhistory}\n\n- Payment amount\nGems: {emote['gems']} {price:,}**",
		   title=f"**{emote['yes']} done successfully**"
		)
		
		del duelData["duels"][date]
		users.Duels_Update(player, duelData)
		users.Update(player, plaerData)
		
		await ctx.reply(embed=embed)
	
	
	#show Member history duels
	async def DuelsHistory(self, ctx: context, player: Member = None):
		
		if player is None:
			player = ctx.author
		
		data = users.Duels_Data(player)
		embeds = []
		count = 0
		embed: Embed = embed_duel_history(player)
		for date in data["duels"]:
				embed.add_field(name=f"{emote['date']} **`{date}`**", value=f"{emote['score']} **{data['duels'][date]}**")
		await ctx.reply(embed=embed)
	
	#normal duel accept
	async def NormalDuel(self, ctx: context, winner: Member, loser: Member, score):
		
		author = ctx.author
		winnerData = users.Load(winner)
		loserData = users.Load(loser)
		
		split_score = score.split("-")
		num1 = int(split_score[0])
		num2 = int(split_score[1])
		score_text = f"{winner.mention} {num1}-{num2} {loser.mention}" if num1 > num2 else f"{winner.mention} {num2}-{num1} {loser.mention}"
		
		self.challenge_functions.ScoreDuel_Save(winner, is_winner=True, score_text=score_text)
		self.challenge_functions.ScoreDuel_Save(player=loser, is_winner=False, score_text=score_text)
		
		winnerGems = randint(300, 500)
		loserGems = randint(150, 300)
		
		winnerData["gems"] += winnerGems
		loserData["gems"] += loserGems
		users.Update(user=winner, data=winnerData)
		users.Update(user=loser, data=loserData)
		
		prize = f"- Winner: {emote['gems']} {winnerGems:,}\n- Loser: {emote['gems']} {loserGems:,}"
		
		await ctx.reply("✓")
		await ctx.send(f"• {winner.mention} {emote['vs']} {loser.mention} •", embed=embed_normal_duels(winner=winner, loser=loser, score_text=score_text, prize=prize))
		
	
	#accept challenge duel
	async def AcceptChallenge(self, ctx: context, winner: Member, loser: Member, score):
		
		if challenges.check(winner) == False and challenges.check(loser) == False:
			await self.functions.ErrorPrefix(errorLog=f"No challenge found {loser.mention} {emote['vs']} {winner.mention}", ctx=ctx)
			return
			
		player = winner if challenges.check(winner) else loser
		data = challenges.Load(player)
		
		if player == winner and data["opponent"] != loser.id:
			await self.functions.ErrorPrefix(errorLog=f"Player {loser.mention} is not part of this challenge. Are you sure you are mentioning the correct player?", ctx=ctx)
			return
		elif player == loser and data["opponent"] != winner.id:
			await self.functions.ErrorPrefix(errorLog=f"Player {winner.mention} is not part of this challenge. Are you sure you are mentioning the correct player?", ctx=ctx)
			return
			
		points = data["points"]
		winnerData = users.Load(winner)
		loserData = users.Load(loser)
		
		winnerData["dp"] += points
		loserData["dp"] -= points
		users.Update(winner, winnerData)
		users.Update(loser, loserData)
		
		split_score = score.split("-")
		num1 = int(split_score[0])
		num2 = int(split_score[1])
		score_text = f"{winner.mention} {num1}-{num2} {loser.mention}" if num1 > num2 else f"{winner.mention} {num2}-{num1} {loser.mention}"
		
		self.challenge_functions.ScoreDuel_Save(winner, is_winner=True, score_text=score_text)
		self.challenge_functions.ScoreDuel_Save(player=loser, is_winner=False, score_text=score_text)
		
		challenges.Delete(player=player)
		
		await ctx.send(f"• {winner.mention} {emote['vs']} {loser.mention} •", embed=embed_challenge_end(winner=winner, loser=loser, score_text=score_text, points=points))
			
	
	#create challenges player vs opponent
	async def Challenge(self, ctx: context, opponent: Member, points):
		
		guild = ctx.guild
		player = ctx.author
		
		if challenges.check(player) == True:
			data = challenges.Load(player)
			opponent = await self.bot.fetch_Member(data["opponent"])
			await self.functions.ErrorPrefix(errorLog=f"Sorry 😅 You already have a challenge registered against {opponent.mention} \n- Challenge points: {emote['points']} {data['points']}", ctx=ctx)
			return
		elif player.id == opponent.id:
			await ctx.reply("https://cdn.discordapp.com/emojis/1037920428510941275.png")
			await ctx.send("**You will play the challenge with yourself, hmmmm great**")
			return	
		elif points > 50:
			await self.functions.ErrorPrefix(errorLog=f"The maximum challenge points is `50` and no higher", ctx=ctx)
			return
		elif points <= 0:
			await self.functions.ErrorPrefix(errorLog=f"Challenge points cannot be 0 or less", ctx=ctx)
			return
		
		embed = self.functions.embed(
		desc=f"Hello {opponent.mention} Do you accept the challenge against the player {player.mention}\n The loser loses {emote['points']} {points} of his points and the winner receives them",
		icon="https://cdn.discordapp.com/emojis/800127196098068501.png",
		title="Duel challenge"
		)
		
		msg = await ctx.reply(f"• {opponent.mention} •", embed=embed)
		await msg.edit(view=ChallengeConfirm(player=player, opponent=opponent, points=points, msg=msg))
		
		
