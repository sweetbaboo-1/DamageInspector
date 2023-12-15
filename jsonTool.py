import json

import settings
logger = settings.logging.getLogger("bot")

def parse(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File not found - {filename}")
    except json.JSONDecodeError:
        print(f"Error: Unable to parse JSON file - {filename}")

def write(filename, content):
  try:  
    with open(filename, "w") as json_file:
      json.dump(content, json_file, indent=2)
      return True
  except Exception as e:
    logger.error(str(e))
    return False