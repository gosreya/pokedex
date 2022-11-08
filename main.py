import requests
import json
import random
import threading

"""

Pokédex: Your personal pocketbook guide to all the Pokémon you'll encounter on your fabulous adventures. 

On launch, the Pokédex will retreive the latest data on all Pokémon from the pokeapi, so you'll always have fresh facts. 

Skills acquired: 
+ multithreading
+ REST API

disclaimer: sometimes here I do wacky things for the sake of implementing something with a new skill instead than an old one

"""

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

  def get_pokemon(self, index):
    req = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{index}/")
    if (req.status_code != 404):
      dat = json.loads(req.text)
      types = self.get_types(dat)
      flavor = self.get_flavor_text(dat)
      profile = {
        "cool_facts": flavor,
        "types": types
      }
      with self._lock:
        self.pokedex[dat["name"]] = profile
  

  def load_dex(self, count):
    threads = []
    for p in range(1, count):
      # YOO WHAT'S THIS???
      t = threading.Thread(target=self.get_pokemon, args=(p,))
      t.start()
      threads.append(t)

    for t in threads:
      t.join()

  
dex = Pokedex()
count = dex.get_pokemon_count()
print("Initializing...")
dex.load_dex(count)
print("complete!\n")

print("Enter a Pokémon's name or enter 'quit' to end the program.\n")

pokemon = input("< What Pokémon would you like to learn about? > ")
while(pokemon != "quit"):
    if not pokemon in dex.pokedex.keys():
      print("\nCould not identify Pokémon.\n")
      pokemon = input("< What Pokémon would you like to learn about? > ")
    else:
      print("\ntypes: ", dex.pokedex[pokemon]["types"], "\n")
      print(random.choice(dex.pokedex[pokemon]["cool_facts"]), "\n")
      pokemon = input("\n< What Pokémon would you like to learn about? > ")


