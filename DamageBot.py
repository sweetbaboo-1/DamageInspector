import requests
import json
import discord
import settings
from discord.ext import commands

playerIDs = {}
# playerIDs["Matt Main"] = 409488410
playerIDs["sweetbaboo"] = 161264304
playerIDs["negative_epsilon"] = 105395680
playerIDs["ambre69"] = 152317231
playerIDs[".artmiss"] = 178855266
playerIDs["galahadtvee"] = 101090810
playerIDs["cursed.one"] = 161133996
playerIDs["hartrun7"] = 439731573

api_get_last_match = "https://api.opendota.com/api/players/#PLAYERID#/matches/?limit=1"
api_match_from_id = "https://api.opendota.com/api/matches/#MATCHID#"

def getDamage(user):
    if user not in playerIDs:
        return f'I\'m sorry {user}, whoever wrote this code forgot about you...'
    
    # Get MatchID
    response = requests.get(api_get_last_match.replace("#PLAYERID#", str(playerIDs[user])))
    
    if response.status_code == 200:
      data = json.loads(response.text)

      if data:
        match_id = data[0].get("match_id")
      else:
        return f'I\'m sorry {user}, I couldn\'t find your most recent match. You probably need to expose public match data...'
      
    else:
        print(f"Error: {response.status_code}")  
        print(response.text)
    
    # Get Damage
    response = requests.get(api_match_from_id.replace("#MATCHID#", str(match_id)))

    if response.status_code == 200:
      data = json.loads(response.text)

      if data:
        damage = {}
        damageBenchmarks = {}
        players = data.get("players")
        for player in players:
          playerID = player.get("account_id")
          for p in playerIDs:
             if playerIDs[p] == playerID:
              damage[p] = player.get("hero_damage")
              damageBenchmarks[p] = player.get("benchmarks").get("hero_damage_per_min")
      else:
        return f'I\'m sorry {user}, something horible has happened. Clearly this was the part written by Chris...'
      
    else:
        print(f"Error: {response.status_code}")  
        print(response.text)
    
    maxDamage = -1
    maxDamagePlayer = ""
    bestPercent = -1
    bestPercentPlayer = ""
    result = f"Match ID: {match_id}\nhttps://www.opendota.com/matches/{match_id}/overview\n"
    
    for player in damage:
      result += f'{player} dealt {damage[player]:,} damage or {round(damageBenchmarks[player].get("raw"), 2):,.2f} damage per minute.\nThat is higher than {round(damageBenchmarks[player].get("pct") * 100, 2)}% of recent players.\n'
      if damage[player] > maxDamage:
        maxDamage = damage[player]
        maxDamagePlayer = player
      if round(damageBenchmarks[player].get("pct") * 100, 2) > bestPercent:
        bestPercent = round(damageBenchmarks[player].get("pct") * 100, 2)
        bestPercentPlayer = player

    result += f'The highest damage was dealt by {maxDamagePlayer} at {maxDamage:,}.\n'
    result += f'The best relative performance was {bestPercentPlayer} who was better than {bestPercent}% of players.'
    return result

def run():
  
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.command()
    async def dmg(ctx):
        """Inspects the damage"""
        await ctx.send("Inspecting the damage...")
        msg = getDamage(ctx.author.name)
        await ctx.send(msg)
  
    bot.run(settings.DISCORD_API_SECRET)

if __name__ == "__main__":
    run()

