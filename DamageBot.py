import discord
import settings
from apiCalls import *
from playerIDs import playerIDs
from discord.ext import commands

logger = settings.logging.getLogger("bot")

api_get_last_match = "https://api.opendota.com/api/players/#PLAYERID#/matches/?limit=1"
api_match_from_id = "https://api.opendota.com/api/matches/#MATCHID#"

def getDamage(user):   
    # Get the most recent match
    recentMatches = getDataFromAPICall(api_get_last_match.replace("#PLAYERID#", str(playerIDs[user])))
    if recentMatches:
      match_id = recentMatches[0].get("match_id")
    else:
      return f'I\'m sorry {user}, I couldn\'t find your most recent match. You probably need to expose public match data...'
    
    # Get damage from match
    recentMatch = getDataFromAPICall(api_match_from_id.replace("#MATCHID#", str(match_id)))

    if recentMatch: # TODO create more interesting metrics.
      damage = {}
      damageBenchmarks = {}
      players = recentMatch.get("players")
      for player in players:
        playerID = player.get("account_id")
        for p in playerIDs:
          if playerIDs[p] == playerID:
            damage[p] = player.get("hero_damage")
            damageBenchmarks[p] = player.get("benchmarks").get("hero_damage_per_min")
    else:
      return f'I\'m sorry {user.nickname}, something horrible has happened. Clearly this was the part written by Chris...'
    
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

    @bot.event
    async def on_ready():
       logger.info(f"User: {bot.user} (ID: {bot.user.id})")

    @bot.command()
    async def dmg(ctx):
        """Inspects the damage"""
        await ctx.send("Inspecting the damage...")
        
        if ctx.author.name not in playerIDs:
          msg = f'I\'m sorry {ctx.author.name}, whoever wrote this code forgot about you...'
        else:
          msg = getDamage(ctx.author.name)
        
        await ctx.send(msg)
  
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()

