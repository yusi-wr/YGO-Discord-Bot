import os
from dotenv import load_dotenv
from nextcord import Embed

load_dotenv()

config = {
    "owners": [1037701642356805723,
    1129456838748942387],
    "prefix": "?",
    "embed-color": 0xff0053,
    "name": "Ash Blossom™",
    "icon": "https://cdn.discordapp.com/attachments/1279166778676744253/1279167363270578278/Haru.Urara.Yu-Gi-Oh.600.3244702.jpg",
    "tourna-icon": "https://cdn.discordapp.com/emojis/868507366658701734.png",
    
    "game-role":{
       "EDOPro": 1134960979743096832,
       "YGOOmega": 1134961080876142652,
       "DuelBook": 1134961494535180358,
       "Duelnexus": 1134961269099741245,
       "MasterDuel": 1134961743974645871,
       "DuelLinks": 1134961611803742289
    },
    
    "img": {
        "tournament": "https://cdn.discordapp.com/attachments/1279166778676744253/1282074296675733534/1725740399004.jpg",
        "bg": "https://cdn.discordapp.com/attachments/1279166778676744253/1279167362788102205/ash_blossom__joyous_spring__wallpaper__by_nhociory_dggi3rw-fullview.jpg",
        "done": "https://cdn.discordapp.com/emojis/1079031910010978315.png",
        "bg-welcome": "https://cdn.discordapp.com/attachments/1279166778676744253/1279167362788102205/ash_blossom__joyous_spring__wallpaper__by_nhociory_dggi3rw-fullview.jpg",
        "bg-duel": "https://cdn.discordapp.com/attachments/1279166778676744253/1282074284742934695/1725740307722.jpg",
    },
    
    "emoji": {
        "manager": "<:Managers:1279171023907979274>",
        "gems": "<:gems:1281968698260848753>",
        "points": "<:points:1279172002577387541>",
        "star": "<a:star2:1279172467495272491>",
        "duel": "<:Duelist:1281970030313078844>",
        "home": "<:eg_home:1281970241764851805>",
        "join": "<:join:1281970496191205488>",
        "leave": "<:leave:1281970683282456768>",
        "list": "<:list:1282272047329841196>",
        "no": "<:Incorrect:1282027181433819140>",
        "yes": "<:Correct:1282027184281747548>",
        "loading": "<a:Loading_:1282027642173915230>",
        "round": "<:rounds:1282030651947745352>",
        "stats": "<:stats:1282031037446225992>",
         "log": "<:logs:1282031498928848928>",
         "score": "<:score:1282031717833510985>",
         "vs": "<:VS:1282032127105306806>",
         "match-winner": "<:winner:1282032443851018270>",
         "cup": "<a:winnercup:1282032455183892523>",
         "cup-winner": "<:winner:1282032443851018270>",
         "win1": "🥇",
         "win2": "🥈",
         "win3": "🥉",
         "time": "<a:Time:1282032988301037629>",
         "gift": "<a:Giftsylv:1282033250952413327>",
         "verify": "<a:verify:1282033569535098902>",
         "welcome": "<:welcome:1282033844815532064>",
         "date": "<:date:1282034314024058962>",
         "back": "<:Backward:1282034970910658591>",
         "ward": "<:forward:1282034986739961887>",
         "link": "<:Link:1282035337962717245>",
         "ticket": "<:Tickets:1282081859173351556>",
         "close": "<:closed:1282038999988441261>",
         "EDOPro": "<:EDOPro:1282070162912186402>",
	     "YGOOmega": "<:Platform_YGOOmega:1282070406546591744>",
	     "DuelBook": "<:DuelingBook:1282070603100061750>",
	     "Duelnexus": "<:DuelingNexus:1282070627729150003>",
	     "MasterDuel": "<:Master_duel:1282070899545215068>",
	     "DuelLinks": "<:DuelLinks:1282071113051930648>",
	     "latency": "<a:Latency:1282039615204622346>",
        
        "cmd": {
           "general": "<:General:1282048771395424379>",
           "tournaments": "<:tournament:1282049060639080530>",
           "admin": "<:admin_administator:1282064600271028307>",
           "ygo": "<:yugioh:1282065150278635530>"
        },
        
        "ranks": {
           "iron": "<:rank_iron:1282066190297989131> Iron",
           "bronze": "<:bronze:1282066504392642650> Bronze",
           "silver": "<:Silver:1282066828029591623> Silver",
           "gold": "<:gold:1282067052189712536> Gold",
           "platinum": "<:platinum:1282067255856861235> Platinum",
           "daimond": "<:Daimond:1282067484005892107> Daimond",
           "master": "<:MasterRank:1282067745839517786> Master",
           "legend": "<:06LegendaryRank:1282068375907860575> Legend",
           "noob": "<a:noob:1282069465470730283> Noob..."
        },
        
        "number": {
            1: "<:number_1:1244623220338982952>",
            2: "<:number_2:1244623324177240126>",
            3: "<:number_3:1244623459816837161>",
            4: "<:number_4:1244623598195314730>",
            5: "<:number_5:1244623677056745482>",
            6: "<:number_6:1244623749735776341>",
            7: "<:number_7:1244623834485755984>",
            8: "<:number_8:1244623908389388439>",
            9: "<:number_9:1244623998982029463>",
            10: "<:number_10:1244624070751031368>",
            11: "<:number_11:1244624156050456646>",
            12: "<:number_12:1244624231161925703>",
            13: "<:number_13:1244624319343100004>",
            14: "<:number_14:1244624398443614229>",
            15: "<:number_15:1244624500021264425>",
            16: "<:number_16:1244624577754038332>",
            17: "<:number_17:1244624668951052359>",
            18: "<:number_18:1244624741382225991>",
            19: "<:number_19:1244624855631003651>",
            20: "<:number_20:1244624924971106384>",
            21: "<:number_21:1244624998065373268>",
            22: "<:number_22:1244625065031762015>",
            23: "<:number_23:1244625152222822491>",
            24: "<:number_24:1244625219734212608>",
            25: "<:number_25:1244625295785459742>",
            26: "<:number_26:1244625361707208798>",
            27: "<:number_27:1244625429864779837>",
            28: "<:number_28:1244625521531424849>",
            29: "<:number_29:1244625595946500166>",
            30: "<:number_30:1244625669699272775>"
        }
    },
}


loading = Embed(description=f"**{config['emoji']['loading']} Loading...**", color=config["embed-color"])