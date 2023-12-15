from heroIDs import getHeroNameFromID
from playerIDs import getPlayerIDs

# TODO: make Dino come up with something more interesting
def parseMatchData(recentMatch, match_id): 
  playerIDs = getPlayerIDs()
  damage = {}
  damageBenchmarks = {}
  heroNames = {}
  players = recentMatch.get("players")
  for player in players:
    playerID = player.get("account_id")
    for p in playerIDs:
      if playerIDs[p] == playerID:
        damage[p] = player.get("hero_damage")
        damageBenchmarks[p] = player.get("benchmarks").get("hero_damage_per_min")
        heroNames[p] = getHeroNameFromID(player.get("hero_id"))
  
  maxDamage = -1
  maxDamagePlayer = ""
  maxDamageHero = ""
  bestPercent = -1
  bestPercentPlayer = ""
  bestPercentHero = ""
  result = f"Match ID: {match_id}\nhttps://www.opendota.com/matches/{match_id}/overview\n"
  
  for player in damage:
    result += f'{player} dealt {damage[player]:,} damage or {round(damageBenchmarks[player].get("raw"), 2):,.2f} damage per minute.\nThat is higher than {round(damageBenchmarks[player].get("pct") * 100, 2)}% of recent players.\n'
    if damage[player] > maxDamage:
      maxDamage = damage[player]
      maxDamagePlayer = player
      maxDamageHero = heroNames[player]
    if round(damageBenchmarks[player].get("pct") * 100, 2) > bestPercent:
      bestPercent = round(damageBenchmarks[player].get("pct") * 100, 2)
      bestPercentPlayer = player
      bestPercentHero = heroNames[player]

  result += f'The highest damage was dealt by {maxDamagePlayer} on {maxDamageHero} at {maxDamage:,}.\n'
  result += f'The best relative performance was {bestPercentPlayer} on {bestPercentHero} who was better than {bestPercent}% of players.'
  return result