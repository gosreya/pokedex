import requests
import json
import random
import threading
from spelling import SpellCorrector

class Pokedex():

  def __init__(self):
    self.pokedex = {}
    self._lock = threading.Lock()

  def get_pokemon_count(self):
    req = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/")
    return(json.loads(req.text)["count"])
  
  def get_flavor_text(self, dat):
    cool_facts = []
    for entry in dat["flavor_text_entries"]:
      cool_facts.append(entry["flavor_text"].replace("\n", " ").replace("\x0c"," "))
      if len(cool_facts) == 10:
        break
    return cool_facts

  def get_types(self, dat):
    types = []
    for entry in dat["egg_groups"]:
      types.append(entry["name"])
    return types

  def get_preevolution(self, dat):
    preforms = None
    if dat["evolves_from_species"]:
      preforms = dat["evolves_from_species"]["name"]
    return preforms

  def get_pokemon(self, index):
    req = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{index}/")
    if (req.status_code != 404):
      dat = json.loads(req.text)
      types = self.get_types(dat)
      flavor = self.get_flavor_text(dat)
      preforms = self.get_preevolution(dat)
      profile = {
        "cool_facts": flavor,
        "types": types,
        "preforms": preforms
      }
      with self._lock:
        self.pokedex[dat["name"]] = profile
  
 """Area for improvement: What is the ideal number of threads?"""
  def load_dex(self, count):
    threads = []
    for p in range(1, count):
      t = threading.Thread(target=self.get_pokemon, args=(p,))
      t.start()
      threads.append(t)

    for t in threads:
      t.join()

  
dex = Pokedex()
count = dex.get_pokemon_count()
print("Initializing...")
dex.load_dex(count)
spell_wizard = SpellCorrector(dex.pokedex.keys())
print("complete!\n")

print("Enter a Pokémon's name or enter 'quit' to end the program.\n")

request = input("< What Pokémon would you like to learn about? > ").lower()
while(request != "quit"):
    pokemon = spell_wizard.correction(request)
    if not pokemon in dex.pokedex.keys():
      print(f"\nCould not identify {request}.\n")
    else:
      if request != pokemon:
        print(f"\nCould not identify {request}. Did you mean {pokemon}?\n")
      print(f"\n{pokemon.upper()}\n")
      print("\ntypes: ", dex.pokedex[pokemon]["types"], "\n")
      print(random.choice(dex.pokedex[pokemon]["cool_facts"]), "\n")
      if dex.pokedex[pokemon]["preforms"]:
        print("Evolves from", dex.pokedex[pokemon]["preforms"], "\n")
    request = input("\n< What Pokémon would you like to learn about? > ").lower()

print("See you later!")


