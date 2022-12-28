# pokedex

A wild Pikachu appeared! 

```text
`;-.          ___,
  `.`\_...._/`.-"`
    \        /      ,
    /()   () \    .' `-._
   |)  .    ()\  /   _.'
   \  -'-     ,; '. <
    ;.__     ,;|   > \
   / ,    / ,  |.-'.-'
  (_/    (_/ ,;|.<`
    \    ,     ;-`
     >   \    /
    (_,-'`> .'
jgs      (_,'
```


Luckily you have **pokedex**, your personal command line guidebook to the world of Pokémon.

Call ```pokedex <pokemon>``` to get the Pokémon's profile. Don't know how to spell the Pokémon's name? No worries, the pokedex has a ***built in spell correction***.



<img src="https://github.com/gosreya/pokedex/blob/main/pokedex/images/usecase.png" alt="pokedex use case" style="width:70%;height: auto;">

<img src="https://github.com/gosreya/pokedex/blob/main/pokedex/images/help.png" alt="pokedex help output" style="width:70%;height: auto;">


## Installation

**Option 1: Use pip**

```
pip install "git+https://github.com/gosreya/pokedex.git"
```

**Option 2: Run a bash script**

For Unix environments:

Place the folder 'pokedex' in a convenient directory, like '/usr/local/etc/', and place the following script in 'usr/local/bin' (replacing the file path with the one you choose).

```
#!/bin/bash

a=$1
b=$2
/usr/local/etc/pokedex/main.py $a $b
```

**Option 3: Don't install it**

Use the Pokedex w/ no hassle on [Replit](https://replit.com/@SreyaGogineni1/POKEDEX#main.py) (Just click 'Run').

## Credits

All Pokémon data is retrieved from the [pokeapi](https://pokeapi.co/).
 
All ASCII art used in the Pokedex was created by Maija Haavisto, and all art (including the above Pikachu for which I have not found the creditee) was taken from the [ASCII Art Archive](https://www.asciiart.eu/).
