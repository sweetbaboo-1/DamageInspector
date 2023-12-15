import settings

from apiCalls import *
from matchDataParser import *
from playerIDs import getPlayerIDs

PLAYER_ID_KEY = "#PLAYER_ID#"
MATCH_ID_KEY = "MATCH_ID"
MATCH_COUNT_KEY = "MATCH_COUNT"

API_GET_LAST_MATCH = f"https://api.opendota.com/api/players/{PLAYER_ID_KEY}/matches/?limit={MATCH_COUNT_KEY}"
API_MATCH_FORM_ID = f"https://api.opendota.com/api/matches/{MATCH_ID_KEY}"


def getDamage(user, match_count):
    logger = settings.logging.getLogger("bot")

    playerIDs = getPlayerIDs()

    # TODO: Allow for multiple matches to be inspected
    if match_count != 1:
        match_count = 1
        logger.warning(f"{user} tried to parse multiple matches")

    # Need to make sure no one tries to parse so many matches that bad things happen.
    if match_count > 10:
        match_count = 1
        logger.warning(f"{user} requested > 10 matches")

    url = API_GET_LAST_MATCH.replace(PLAYER_ID_KEY, str(playerIDs[user.name])).replace(
        MATCH_COUNT_KEY, str(match_count)
    )

    # Get the most recent matches
    recentMatches = getDataFromAPICall(url)

    # get the match ids
    if not recentMatches:
        return f"I'm sorry {user.nick}, I couldn't find your most recent match. You probably need to expose public match data..."

    match_id = recentMatches[0].get(
        "match_id"
    )  # TODO: Allow for multiple matches to be inspected

    # Get match data
    url = API_MATCH_FORM_ID.replace(MATCH_ID_KEY, str(match_id))
    recentMatch = getDataFromAPICall(url)

    if not recentMatch:
        logger.error(f"Recent match was None")
        return f"I'm sorry {user.nick}, something horrible has happened. Clearly this was the part written by Chris..."

    return parseMatchData(recentMatch, match_id)
