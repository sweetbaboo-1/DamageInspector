import requests
import json

def getAPIResponse(url):
   return requests.get(url)

def getDataFromAPICall(url):
   response = getAPIResponse(url)
   if response.status_code == 200:
      data = json.loads(response.text)
      return data
   else:
    print(f"Error: {response.status_code}")  
    print(response.text)
    return None