#!/usr/bin/env python3
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json
import random
import threading
import argparse
import os
import pathlib
import concurrent.futures
from pokedex.spelling.spelling import SpellCorrector
import time

POKEGALLERY = {
    "pikachu": """
                                               ,-.
                                          _.|  '
                                        .'  | /
                                      ,'    |'
                                     /      /
                       _..----""---.'      /
 _.....---------...,-""                  ,'
 `-._  \                                /
     `-.+_            __           ,--. .
          `-.._     .:  ).        (`--"| \\
               7    | `" |         `...'  \\
               |     `--'     '+"        ,". ,""-
               |   _...        .____     | |/    '
          _.   |  .    `.  '--"   /      `./     j
         \' `-.|  '     |   `.   /        /     /
         '     `-. `---"      `-"        /     /
          \       `.                  _,'     /
           \        `                        .
            \                                j
             \                              /
              `.                           .
                +                          \\
                |                           L
                |                           |
                |  _ /,                     |
                | | L)'..                   |
                | .    | `                  |
                '  \'   L                   '
                 \  \   |                  j
                  `. `__'                 /
                _,.--.---........__      /
               ---.,'---`         |   -j"
                .-'  '....__      L    |
              ""--..    _,-'       \ l||
                  ,-'  .....------. `||'
               _,'                /
             ,'                  /
            '---------+-        /
                     /         /
                   .'         /
                 .'          /
               ,'           /
             _'....----\"\"\""" mh
  """,
    "squirtle": """
                 _,........__
            ,-'            "`-.
          ,'                   `-.
        ,'                        \\
      ,'                           .
      .'\\               ,"".       `
     ._.'|             / |  `       \\
     |   |            `-.'  ||       `.
     |   |            '-._,'||       | \\
     .`.,'             `..,'.'       , |`-.
     l                       .'`.  _/  |   `.
     `-.._'-   ,          _ _'   -" \\  .     `
`.\"\"\"""'-.`-...,---------','         `. `....__.
.'        `"-..___      __,'\\          \\  \\     \\
\_ .          |   `\"\"\""'    `.           . \\     \\
  `.          |              `.          |  .     L
    `.        |`--...________.'.        j   |     |
      `._    .'      |          `.     .|   ,     |
         `--,\\       .            `7""' |  ,      |
            ` `      `            /     |  |      |    _,-'\"""`-.
             \\ `.     .          /      |  '      |  ,'          `.
              \\  v.__  .        '       .   \\    /| /              \\
               \\/    `""\"\""\"\"""`.       \\   \\  /.''                |
                `        .        `._ ___,j.  `/ .-       ,---.     |
                ,`-.      \\         ."     `.  |/        j     `    |
               /    `.     \\       /         \\ /         |     /    j
              |       `-.   7-.._ .          |"          '         /
              |          `./_    `|          |            .     _,'
              `.           / `----|          |-............`---'
                \\          \\      |          |
               ,'           )     `.         |
                7____,,..--'      /          |
                                  `---.__,--.'mh
  """,
    "bulbasaur": """ 
                                             /
                        _,.------....___,.' ',.-.
                     ,-'          _,.--"        |
                   ,'         _.-'              .
                  /   ,     ,'                   `
                 .   /     /                     ``.
                 |  |     .                       \\.\\
       ____      |___._.  |       __               \\ `.
     .'    `---""       ``"-.--"'`  \\               .  \\
    .  ,            __               `              |   .
    `,'         ,-"'  .               \\             |    L
   ,'          '    _.'                -._          /    |
  ,`-.    ,".   `--'                      >.      ,'     |
 . .'\\'   `-'       __    ,  ,-.         /  `.__.-      ,'
 ||:, .           ,'  ;  /  / \\ `        `.    .      .'/
 j|:D  \\          `--'  ' ,'_  . .         `.__, \\   , /
/ L:_  |                 .  "' :_;                `.'.'
.    ""'                  \"\"\"""'                    
 `.                                 .    `.   _,..  `
   `,_   .    .                _,-'/    .. `,'   __  `
    ) \`._        ___....----"'  ,'   .'  \ |   '  \  .
   /   `. "`-.--"'         _,' ,'     `---' |    `./  |
  .   _  `""'--.._____..--"   ,             '         |
  | ." `. `-.                /-.           /          ,
  | `._.'    `,_            ;  /         ,'          .
 .'          /| `-.        . ,'         ,           ,
 '-.__ __ _,','    '`-..___;-...__   ,.'\ ____.___.'
 `"^--'..'   '-`-^-'"--    `-^-'`.''\"\"\"""`.,^.`.--' mh
  """,
    "charmander": """
                _.--""`-..
            ,'          `.
          ,'          __  `.
         /|          " __   \\
        , |           / |.   .
        |,'          !_.'|   |
      ,'             '   |   |
     /              |`--'|   |
    |                `---'   |
     .   ,                   |                       ,".
      ._     '           _'  |                    , ' \\ `
  `.. `.`-...___,...---""    |       __,.        ,`"   L,|
  |, `- .`._        _,-,.'   .  __.-'-. /        .   ,    \\
-:..     `. `-..--_.,.<       `"      / `.        `-/ |   .
  `,         \"\"""'     `.              ,'         |   |  ',,
    `.      '            '            /          '    |'. |/
      `.   |              \\       _,-'           |       ''
        `._'               \\   '"\\                .      |
           |                '     \\                `._  ,'
           |                 '     \\                 .'|
           |                 .      \\                | |
           |                 |       L              ,' |
           `                 |       |             /   '
            \                |       |           ,'   /
          ,' \               |  _.._ ,-..___,..-'    ,'
         /     .             .      `!             ,j'
        /       `.          /        .           .'/
       .          `.       /         |        _.'.'
        `.          7`'---'          |------"'_.'
       _,.`,_     _'                ,''-----"'
   _,-_    '       `.     .'      ,\\
   -" /`.         _,'     | _  _  _.|
    ""--'---\"\"\"""'        `' '! |! /
                            `" " -' mh
  """,
}


class Pokedex():

    def __init__(self):
        self.pokecount = 0
        self.evocount = 0
        self.pokedex = {}
        self._lock = threading.Lock()
        self._evolock = threading.Lock()
        directory = os.path.dirname(os.path.realpath(__file__))
        self.pokefile = pathlib.Path(directory) / "pokefile.json"
        self.evolutions = {}

    def get_pokemon_count(self):
        url = "https://pokeapi.co/api/v2/pokemon-species/"
        request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request_site) as response:
            req = json.loads(response.read())
        self.pokecount = req["count"]

        url = "https://pokeapi.co/api/v2/evolution-chain/"
        request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request_site) as response:
            req = json.loads(response.read())
        self.evocount = req["count"]


    def get_flavor_text(self, dat):
        cool_facts = []
        for entry in dat["flavor_text_entries"]:
            if entry["language"]["name"] == "en":
                cool_facts.append(
                    entry["flavor_text"].replace("\n", " ").replace("\x0c",
                                                                    " "))
            if len(cool_facts) == 10:
                break
        return cool_facts

    def get_types(self, dat):
        types = []
        for entry in dat["egg_groups"]:
            types.append(entry["name"])
        return types

    def get_evolution(self, index):
        url = f"https://pokeapi.co/api/v2/evolution-chain/{index}/"
        evolution_chain = []
        request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urlopen(request_site) as response:
                dat = json.loads(response.read())["chain"]
                while True:
                    evolution_chain.append(dat["species"]["name"])
                    if dat["evolves_to"] == []:
                        break
                    dat = dat["evolves_to"][0]
        except HTTPError:
            pass
        with self._evolock:
            self.evolutions[url] = evolution_chain
        return

    def get_pokemon(self, index):
        url = f"https://pokeapi.co/api/v2/pokemon-species/{index}/"
        request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urlopen(request_site) as response:
                dat = json.loads(response.read())
        except HTTPError:
            return
        types = self.get_types(dat)
        flavor = self.get_flavor_text(dat)
        evolutions_url = dat["evolution_chain"]["url"]
        if evolutions_url in self.evolutions:
            evolutions = self.evolutions[evolutions_url]
        else:
            evolutions = None
        profile = {
            "cool_facts": flavor,
            "types": types,
            "evolutions": evolutions
        }
        with self._lock:
            self.pokedex[dat["name"]] = profile

    def load_dex(self):
        self.get_pokemon_count()

        indices = range(1, self.evocount + 1)
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            executor.map(self.get_evolution, indices)

        indices = range(1, self.pokecount + 1)
        with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
            executor.map(self.get_pokemon, indices)

    def update_file(self):
        print("Updating pokefile...")
        self.load_dex()
        with open(self.pokefile, "w") as pokefile:
            pokefile.write(json.dumps(self.pokedex))

    def evo_name(self, name, pokemon):
        if name == pokemon:
            return f"\33[7m {name.upper()} \x1b[0m"
        else:
            return name.upper()


    def answer(self, request):
        with open(self.pokefile, "r") as pokefile:
            self.pokedex = json.loads(pokefile.read())
        spell_wizard = SpellCorrector(self.pokedex.keys())
        if request.lower() == "random":
            pokemon = random.choice([name for name in self.pokedex.keys()])
        else:
            pokemon = spell_wizard.correction(request.lower())
        if not pokemon in self.pokedex.keys():
            print(f"\nCould not identify '{request}'.\n")
        else:
            if request != pokemon and request.lower() != "random":
                print(
                    f"\nCould not identify '{request}'. Did you mean '{pokemon}'?")
            print(f"\n> {self.evo_name(pokemon, pokemon)}\n")
            evolution = ""
            if len(self.pokedex[pokemon]["evolutions"]) > 1:
                evolution = "|| "
                evolution += " -> ".join(self.evo_name(name, pokemon) for name
                                         in
                                         self.pokedex[
                    pokemon]["evolutions"])
            print(f"> types: {self.pokedex[pokemon]['types']} {evolution}\n")
            print(f"> {random.choice(self.pokedex[pokemon]['cool_facts'])}\n")
            if pokemon in POKEGALLERY:
                print(POKEGALLERY[pokemon])


def usage_message():
    return "pokedex [-h] [-u] [pokemon]"


def query():
    parser = argparse.ArgumentParser(description="Get any pokemon's profile.",
                                     usage=usage_message())
    parser.add_argument("pokemon", type=str, nargs='?',
                        help="name a pokemon, or type 'random'")
    parser.add_argument("-u", "--update", action='store_true',
                        help="update the pokemon list with the latest records")
    args = parser.parse_args()
    if args.pokemon or args.update:
        dex = Pokedex()
        if args.update:
            dex.update_file()
        if args.pokemon:
            dex.answer(args.pokemon)


if __name__ == "__main__":
    query()
