from jsonTool import parse, write
from settings import HERO_INFO_FILENAME


def getHeroData():
    return parse(HERO_INFO_FILENAME)


def getHeroNameFromID(id):
    data = parse(HERO_INFO_FILENAME)
    heroID = str(id)
    if data[heroID] is not None:
        return data[heroID]


def getHeroIDFromName(name):
    data = parse(HERO_INFO_FILENAME)
    for key in data:
        if data[key] == name:
            return key
    return -1


def addHero(id, name) -> bool:
    data = parse(HERO_INFO_FILENAME)
    data[id] = name
    return write(HERO_INFO_FILENAME, data)


def removeHero(name) -> bool:
    id = getHeroIDFromName(name)
    if id < 0:
        return False
    data = parse(HERO_INFO_FILENAME)
    del data[id]
    return write(HERO_INFO_FILENAME, data)
