import requests
import json
import settings

logger = settings.logging.getLogger("bot")


def getAPIResponse(url):
    return requests.get(url)


def getDataFromAPICall(url):
    response = getAPIResponse(url)
    logger.info(f"Making API call to {url}")
    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        logger.error(f"{response.status_code} {response.text}")
        return None
