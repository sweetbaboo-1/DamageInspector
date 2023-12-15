from jsonTool import parse, write
from settings import PLAYER_INFO_FILENAME

def getPlayerIDs():
  player_data = parse(PLAYER_INFO_FILENAME)
  return player_data
     
def addPlayer(name, id) -> bool:
  data = parse(PLAYER_INFO_FILENAME)
  data[name] = id
  return write(PLAYER_INFO_FILENAME, data)

def removePlayer(name) -> bool:
  data = parse(PLAYER_INFO_FILENAME)
  del data[name]
  return write(PLAYER_INFO_FILENAME, data)