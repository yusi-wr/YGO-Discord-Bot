from nextcord.ext import commands
from nextcord import Interaction, Embed, User, Color, PermissionOverwrite
from .functions import FunctuonsTourna
from .embeds import embed_log, embed_tounaments, embed_log_match
from database import Load, tournaments
from .views import ConfirmExclude, ConfirmQualify
from config import config
import os
from core.functions import Functions

emote = config["emoji"]

def check_has_tourna(user: User):
	if f"{str(user.id)}.json" in os.listdir("./database/data/tournaments/"):
		return True
	else:
		return False

class CommandTourna:
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.functions = FunctuonsTourna(self.bot)
		self.functionsHelp = Functions(self.bot)
	
	
	# function for ending tournament
	async def EndTournament(self, ctx: commands.Context, winner: User, winner2: User, winner3: User = None):
		
		manager = ctx.author
		
		if not check_has_tourna(manager):
			await self.functionsHelp.ErrorPrefix(f"{emote['no']} Sorry, you are not currently supervising any tournament", ctx=ctx)
			return
			
		data = tournaments.Load(manager)
		
		try:
			await self.functions.EndTourna(manager=manager, data=data, winner=winner, winner2=winner2, winner3=winner3)
			
			await ctx.reply(embed=self.functionsHelp.embed(desc="The tournament was successfully completed and everyone was informed of its results. Thank you", icon=ctx.author.avatar.url))
		except AttributeError as ER:
			await self.functionsHelp.ErrorPrefix(errorLog=f"```{ER}```",ctx=ctx)
	
	
	#function delete tournaments
	async def DeleteTournament(self, ctx: commands.Context, reason = None):
		manager = ctx.author
		
		if not check_has_tourna(manager):
			await self.functionsHelp.ErrorPrefix(f"{emote['no']} Sorry, you are not currently supervising any tournament", ctx=ctx)
			return
			
		data = tournaments.Load(manager)
		
		if data["round"] == "final" and len(data["current-round"]) == 0 and len(data["next-round"]) == 1:
			await self.functionsHelp.ErrorPrefix(errorLog=f"I apologize, my friend, but the tournament has already ended and the final has been confirmed: {data['log']['final'][0] if 'final' in data['log'] else '-'}\nUse: `?t-end` to announce the end of the tournament\nExample: ```?t-end @winner @s2 @s3```", ctx=ctx)
			return
		
		if reason == None:
			reason = "The reason is not known..."
			
		guild = await self.bot.fetch_guild(data["guild"])
		channel_announce = await guild.fetch_channel(data["channel_announce"])
		channel_log = await guild.fetch_channel(data["log_channel"])
		
		msg_announce = await channel_announce.fetch_message(data["msg_announce"])
		
		role = guild.get_role(data["role"])
		name = data["name"]
		
		embed = embed_tounaments(
		   name=name,
		   desc=f"The tournament has been deleted/cancelled. We apologize to everyone participating in this tournament 🙂\n- Reason: ```{reason}```\nFor more details, please contact the organizer 👇",
		   manager=manager
		)
		
		await msg_announce.edit(embed=embed, view=None)
		await channel_announce.send(f"{role.mention}")
		if len(data["log"]) >= 1:
			await channel_log.send(embed=embed_log(manager))
		await role.delete()
		
		os.remove(f"./database/data/tournaments/{str(manager.id)}.json")
		
		await ctx.reply(embed=self.functionsHelp.embed(desc="The tournament has been successfully deleted. Thank you", icon=config["tourna-icon"], title=f"{emote['cup']} **{name}** {emote['cup']}"))
	
	#function for qualify of players
	async def QualifyPlayer(self, ctx: commands.Context, player: User):
		
		manager = ctx.author
		if not check_has_tourna(manager):
			await self.functionsHelp.ErrorPrefix(f">>> **{emote['no']} Sorry, you are not currently supervising any tournament**", ctx=ctx)
			return
		data = tournaments.Load(manager)
		
		if data["round"] == "final" and len(data["current-round"]) == 0 and len(data["next-round"]) == 1:
			await self.functionsHelp.ErrorPrefix(errorLog=f"I apologize, my friend, but the tournament has already ended and the final has been confirmed: {data['log']['final'][0] if 'final' in data['log'] else '-'}\nUse: `?t-end` to announce the end of the tournament\nExample: ```?t-end @winner @s2 @s3```", ctx=ctx)
			return
		
		if player.id in data["current-round"]:
				reply = f"The player {player.mention} from the competitors in the current round has not been confirmed for his match against his opponent.\nAre you sure he qualifies?"
				msg = await ctx.reply(embed=self.functionsHelp.embed(desc=reply))
				await msg.edit(view=ConfirmQualify(manager=manager, player=player, msg=msg))
				
		elif player.id in data["leave"]:
				reply = f"Player {player.mention}. Excluded by losing a match or by: `?t-exclude`\nAre you sure you want him to qualify?"
				msg = await ctx.reply(embed=self.functionsHelp.embed(desc=reply))
				await msg.edit(view=ConfirmQualify(manager=manager, player=player, msg=msg))
				
		else:
				players_leave = [await self.bot.fetch_user(x) for x in data["next-round"]]
				players = "- " + "\n- ".join(x.mention for x in players_leave)
				await self.functionsHelp.ErrorPrefix(errorLog=f"Sorry, but player {player.mention}. Already qualified for the next round\n- {emote['yes']} *Qualified for the next round ↓*\n{players}", ctx=ctx)
		
	
	#fucntion command Exclude player
	async def ExcludePlayer(self, ctx: commands.Context, player: User):
		
		manager = ctx.author
		if not check_has_tourna(manager):
			await self.functionsHelp.ErrorPrefix(f"{emote['no']} Sorry, you are not currently supervising any tournament", ctx=ctx)
			return
		data = tournaments.Load(manager)
		
		if data["round"] == "final" and len(data["current-round"]) == 0 and len(data["next-round"]) == 1:
			await self.functionsHelp.ErrorPrefix(errorLog=f"I apologize, my friend, but the tournament has already ended and the final has been confirmed: {data['log']['final'][0] if 'final' in data['log'] else '-'} \nUse: `?t-end` to announce the end of the tournament\nExample: ```?t-end @winner @s2 @s3```", ctx=ctx)
			return
		
		if data["is_started"] == False:
			reply = f"Players may not be excluded before the rounds begin. They can only be unsubscribed by: ?t-remove"
			await self.functionsHelp.ErrorPrefix(errorLog=reply, ctx=ctx)
			return
		
		if player.id in data["current-round"]:
			reply = f"I apologize for asking: Are you sure the player will excluded? {player.mention}\nThe results of the player's match have not been confirmed and he does not qualify for the next round."
			msg = await ctx.reply(embed=self.functionsHelp.embed(desc=reply))
			await msg.edit(view=ConfirmExclude(manager=manager, player=player, msg=msg))
			
		elif player.id in data["next-round"]:
			reply = f"Hello organiser.\nThe player {player.mention} is one of the qualifiers for the next round of the tournament.\nAre you sure he will be excluded?"
			msg = await ctx.reply(embed=self.functionsHelp.embed(desc=reply))
			await msg.edit(view=ConfirmExclude(manager=manager, player=player, msg=msg))
			
		else:
			players_leave = [await self.bot.fetch_user(x) for x in data["leave"]]
			players = "- " + "\n- ".join(x.mention for x in players_leave)
			await self.functionsHelp.ErrorPrefix(errorLog=f"Sorry, but the player You want to exclude is already out of the competition\n- {emote['no']} *Out of the league ↓*\n{players}", ctx=ctx)
	
	
	#confirm match and save to log
	async def MatchConfirm(self, ctx: commands.Context,winner: User, loser: User, match_sorce):
		
		manager = ctx.author
		if not check_has_tourna(manager):
			await self.functionsHelp.ErrorPrefix(f"{emote['no']} Sorry, you are not currently supervising any tournament", ctx=ctx)
			return
		data = tournaments.Load(manager)
		
		if data["round"] == "final" and len(data["current-round"]) == 0:
			await self.functionsHelp.ErrorPrefix(errorLog=f"I apologize, my friend, but the tournament has already ended and the final has been confirmed: {data['log']['final'][0] if 'final' in data['log'] else '-'}\nUse: `?t-end` to announce the end of the tournament\nExample: ```?t-end @winner @s2 @s3```", ctx=ctx)
			return
		
		#simple function for help
		def function_check(player, data_list):
			
			if player.id in data[data_list]:
				return True
			else:
				return False
			
		if function_check(winner, "leave"):
			await self.functionsHelp.ErrorPrefix(errorLog=f"Player {winner.mention} is out of competition", ctx=ctx)
			return
		elif function_check(loser, "leave"):
			await self.functionsHelp.ErrorPrefix(errorLog=f"Player {loser.mention} is out of competition", ctx=ctx) 
			return
			
		if function_check(winner, "next-round"):
			await self.functionsHelp.ErrorPrefix(errorLog=f"Sorry, but player {winner.mention} is already on the list of candidates for the next round", ctx=ctx)
			return
		elif function_check(loser, "next-round"):
			await self.functionsHelp.ErrorPrefix(errorLog=f"Sorry, but player {loser.mention} is already on the list of candidates for the next round", ctx=ctx)
			return
			
		if not function_check(winner, "current-round"):
			await self.functionsHelp.ErrorPrefix(errorLog=f"The player {winner.mention} is not one of the players in the current round", ctx=ctx)
			return
		elif not function_check(loser, "current-round"):
			await self.functionsHelp.ErrorPrefix(errorLog=f"The player {loser.mention} is not one of the players in the current round", ctx=ctx)
			return
		
		
		score = str(match_sorce).split("-")
		num1 = int(score[0])
		num2 = int(score[1])
		if num1 > num2:
			text_score = f"{winner.mention} {num1}-{num2} {loser.mention}"
		else:
			text_score = f"{loser.mention} {num1}-{num2} {winner.mention}"
				
		await self.functions.ResultMatchSave(manager=manager, log_match=text_score, winner=winner, loser=loser)
		
		channel_log = await self.bot.fetch_channel(data["log_channel"])
		
		embed_match: Embed = embed_log_match(log_match=text_score, name=data["name"], winner=winner)
		embed_match.add_field(name=f"{emote['win1']} {winner.mention}", value=f">>> **{self.functions.MatchPrize(player=winner, is_winner=True)}**")
		embed_match.add_field(name=f"{emote['win2']} {loser.mention}", value=f">>> **{self.functions.MatchPrize(player=loser, is_winner=False)}**")
		
		await channel_log.send(f"**- {emote['round']} Round: {data['round']}\n• {winner.mention} {emote['vs']} {loser.mention} •**", embed=embed_match)
		
		await ctx.reply(embed=self.functionsHelp.embed(desc=f"The result of a match between {winner.mention} and {loser.mention} has been successfully saved and announced\n- The round: `{data['round']}`"))
		
	
	#remove user from tournaments befor start
	async def RomverUser(self, ctx: commands.Context, user: User):
		
		manager = ctx.author
		if not check_has_tourna(manager):
			await self.functionsHelp.ErrorPrefix(f"{emote['no']} Sorry, you are not currently supervising any tournament", ctx=ctx)
			return
		
		data = tournaments.Load(manager)
		if data["is_started"] == True:
			await self.functionsHelp.ErrorPrefix(f"This is to remove a player from the tournament Permanently before the first draw in the tournament begins, it cannot be used after that to exclude a player. Use: `?t-exclude @user`", ctx=ctx)
			return
		if not user.id in data["participants"]:
			await self.functionsHelp.ErrorPrefix(f"No, this user is not in the list of participants in this tournament", ctx=ctx)
			return
			
		try:
			await self.functions.RemovePlayer(manager, user)
			embed = self.functionsHelp.embed(desc=f"The player has been successfully removed from the tournament completely", title="Done successfully")
			await ctx.reply(embed=embed)
		except AttributeError as ER:
			await self.functionsHelp.ErrorPrefix(errorLog=f"```{ER}```", ctx=ctx)
	
	#function command start rounds
	async def StartRound(self, ctx: commands.Context):
		
		manager = ctx.author
		
		if not check_has_tourna(manager):
			await self.functionsHelp.ErrorPrefix(f"{emote['no']} Sorry, you are not currently supervising any tournament", ctx=ctx)
			return 
			
		data = tournaments.Load(manager)
		
		if data["round"] == "final":
			await self.functionsHelp.ErrorPrefix(errorLog=f"I apologize, my friend, but the tournament has already ended and the final has been confirmed: {data['log']['final'][0] if 'final' in data['log'] else '-'}\nUse: `?t-end` to announce the end of the tournament\nExample: ```?t-end @winner @s2 @s3```", ctx=ctx)
			return
		
		if not data["is_started"] == True:
			participants = data["participants"]
			count_participants = len(participants)
			if count_participants % 2 != 0:
				await ctx.reply(f"Sorry, the first round of the tournament cannot start. We are missing: `{count_participants % 2}`\nParticipants: `{count_participants}`\nUse: ?t-remove | `To remove one of the participants`")
				return
			
			try:
				await self.functions.Start_Round(manager)
				await ctx.reply(embed=Embed(description=f"The announcement was made and the round started successfully. Good luck to all players", color=config["embed-color"]))
			except AttributeError as Error:
				await self.functionsHelp.ErrorPrefix(errorLog=f"```{Error}```", ctx=ctx)
				
		else:
			round = data["round"]
			current_round = data["current-round"]
			next_round = data["next-round"]
			
			if len(current_round) != 0:
				await self.functionsHelp.ErrorPrefix(f"The round `{round}` cannot start. There are `{len(current_round)}` players in the current round whose matches have not been confirmed. Eliminate one of them and one of them qualifies.", ctx=ctx)
				return
			elif len(next_round) % 2 != 0:
				await self.functionsHelp.ErrorPrefix(f"The round cannot start. We do not have enough qualifiers for the next round\nWe are missing a `{len(next_round) % 2}` Player", ctx=ctx)
				return
			elif len(next_round) == 0:
				await self.functionsHelp.ErrorPrefix(f"There are no qualifiers for the next round of the tournament", ctx=ctx)
				return
			try:
				await self.functions.Start_Round(manager)
				await ctx.reply(embed=self.functionsHelp.embed(desc=f"Round `{round + 1}` of tournament `{data['name']}` started successfully.\nGood luck to all players"))
			except AttributeError as Error:
				await self.functionsHelp.ErrorPrefix(errorLog=f"```{Error}```", ctx=ctx)
	
	#slash command create tourna
	async def CreateTourna(self, interaction: Interaction, name: str, desc: str, announc_channel, log_channel):
			msg = await interaction.response.send_message(f">>> {emote['loading']} **Tournament is being created...**", ephemeral=True)
			
			guild = interaction.guild
			role = await guild.create_role(name=f"•🏆 {name} 🏆•", color=Color.random())
			
			manager = interaction.user
			
			overwrite = PermissionOverwrite()
			overwrite.view_channel = True
			overwrite.read_messages = True
		
			await log_channel.set_permissions(role, overwrite=overwrite)
			await announc_channel.set_permissions(role, overwrite=overwrite)
			
			await self.functions.CreateTournament(manager=manager, name=name, channel_announce=announc_channel, desc=desc, role=role, log_channel=log_channel)
			
			await msg.edit(f">>> {emote['yes']} **Your tournament has been successfully created**")