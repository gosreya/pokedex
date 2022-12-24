from urllib.request import Request, urlopen
import requests
import json

url = "https://pokeapi.co/api/v2/pokemon-species/"
request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urlopen(request_site) as response:
    req = json.loads(response.read())
    print(response_content)

req = requests.get("https://pokeapi.co/api/v2/pokemon-species/")
print(json.loads(req.text))
  