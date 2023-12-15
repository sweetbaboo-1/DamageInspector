import discord
import settings
from apiCalls import *
from playerIDs import playerIDs
from discord.ext import commands

logger = settings.logging.getLogger("bot")

PLAYER_ID_KEY = "#PLAYER_ID#"
MATCH_ID_KEY = "MATCH_ID"
MATCH_COUNT_KEY = "MATCH_COUNT"

API_GET_LAST_MATCH = f"https://api.opendota.com/api/players/{PLAYER_ID_KEY}/matches/?limit={MATCH_COUNT_KEY}"
API_MATCH_FORM_ID = F"https://api.opendota.com/api/matches/{MATCH_ID_KEY}"

def parseMatchData(recentMatch, match_id): 
  damage = {}
  damageBenchmarks = {}
  players = recentMatch.get("players")
  for player in players:
    playerID = player.get("account_id")
    for p in playerIDs:
      if playerIDs[p] == playerID:
        damage[p] = player.get("hero_damage")
        damageBenchmarks[p] = player.get("benchmarks").get("hero_damage_per_min")
  
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


def getDamage(user, match_count):
    # TODO: Allow for multiple matches to be inspected
    if match_count != 1:
       match_count = 1
       logger.warning(f"{user} tried to parse multiple matches")
    
    # Need to make sure no one tries to parse so many matches that bad things happen.
    if match_count > 10:
       match_count = 1
       logger.warning(f"{user} requested > 10 matches")

    url = API_GET_LAST_MATCH.replace(PLAYER_ID_KEY, str(playerIDs[user])).replace(MATCH_COUNT_KEY, str(match_count))

    # Get the most recent matches
    recentMatches = getDataFromAPICall(url, logger)
    
    # get the match ids
    if not recentMatches:
      return f'I\'m sorry {user}, I couldn\'t find your most recent match. You probably need to expose public match data...'
    
    match_id = recentMatches[0].get("match_id") # TODO: Allow for multiple matches to be inspected
    
    # Get match data
    url = API_MATCH_FORM_ID.replace(MATCH_ID_KEY, str(match_id))
    recentMatch = getDataFromAPICall(url, logger)

    if not recentMatch:
      logger.error(f"Recent match was None")
      return f'I\'m sorry {user}, something horrible has happened. Clearly this was the part written by Chris...'

    return parseMatchData(recentMatch, match_id)

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
       logger.info(f"User: {bot.user} (ID: {bot.user.id})")

    @bot.command()
    async def dmg(ctx, match_count=1):
        """Inspects the damage"""
        await ctx.send("Inspecting the damage...")
        
        if ctx.author.name not in playerIDs:
          msg = f'I\'m sorry {ctx.author.name}, whoever wrote this code forgot about you...'
        else:
          msg = getDamage(ctx.author.name, match_count)
        
        await ctx.send(msg)
  
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()

