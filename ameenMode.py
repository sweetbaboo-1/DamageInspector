"""
Ameen Mode

The goal of this module is to identify stats or combinations of stats that one could point to in order to claim match MVP.


"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from playerIDs import getPlayerIDs
from heroIDs import getHeroNameFromID


def find_max_stats(all_stats):
    np = "noteable_players"
    noteable_players = all_stats[np]
    exclude = ["hero_id",
               "account_id"]

    max_indices = all_stats.idxmax(axis=0, numeric_only=True)
    max_indices = max_indices.drop(exclude, axis=0)
    
    max_stats_df = pd.DataFrame({
        "Player": [noteable_players[i] for i in max_indices],
        "Stat": max_indices.index,
        "Value": all_stats.max(numeric_only=True).drop(exclude)
    })

    return max_stats_df


def gather_stats(players, playerIDs):
    id = ["hero_id",
          "account_id"]

    # Game Statistics
    # TODO:
    # Any other tracked stats as I find their aliases
    # Stats I've commented don't appear to come with a standard API call...
    game_stats = [
        "hero_damage",
        "kills",
        "kills_per_min",
        "deaths",
        "assists",
        "kda",
        "net_worth",
        "last_hits",
        "gold_per_min",
        "xp_per_min",
        #"tower_kills",
        "tower_damage", 
        #"courier_kills",
        #"observer_kills",
        #"sentry_kills",
        #"roshan_kills",
        #"teamfight",
        #"observer_placed",
        #"sentry_placed",
        #"camps_stacked",
        #"runes_grabbed",
        #"stuns",
        "hero_healing",
        ]
    benchmark_stats = [
        "hero_damage_per_min",
        "last_hits_per_min",
        "hero_healing_per_min",
    ]

    benchmark_stats_names = [None]*2*len(benchmark_stats)
    benchmark_stats_names[::2] = benchmark_stats
    benchmark_stats_names[1::2] = [i + "_pct" for i in benchmark_stats]
    
    stats = id + game_stats + benchmark_stats_names
    
    all_stats = []
    damage = {}
    damageBenchmarks = {}
    heroNames = {}
    
    for player in players:
        playerID = player.get("account_id")
        
        # The code Matt wrote, kept here for backwards compatibility:
        for p in playerIDs:
            if playerIDs[p] == playerID:
                damage[p] = player.get("hero_damage")

                damageBenchmarks[p] = player.get("benchmarks").get(
                    "hero_damage_per_min",
                    )
                heroNames[p] = getHeroNameFromID(player.get("hero_id"))
    
        # Generate a dataframe with all of the stats aligned
        row = []
        for stat in id+game_stats:
            row.append(player.get(stat))
        
        # Creates different column for raw and pct stats
        for benchmark_stat in benchmark_stats:
            bs = player.get("benchmarks").get(benchmark_stat)
            raw = bs["raw"]
            pct = bs["pct"]
            row += [raw, pct]
        
        all_stats.append(row)

    inv_map = {v: k for k, v in playerIDs.items()}


    all_stats_df = pd.DataFrame(all_stats, columns=stats)
    all_stats_df = all_stats_df.assign(
        hero_name = lambda x: [getHeroNameFromID(id) for id in x.hero_id],
        noteable_players = lambda x: [inv_map[id] if id in inv_map else pd.NA for id in x.account_id]
        )

    return all_stats_df, damage, damageBenchmarks, heroNames
        
