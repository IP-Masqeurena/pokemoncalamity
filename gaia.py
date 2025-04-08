# data.py
# This file contains the Pokémon data and global constants.

# Multipliers used for calculations.
POKEBALL_MULTIPLIER = 1.0
MEDAL_MULTIPLIER = 1.0
TYPE_MULTIPLIER = 1.0

# Pokémon data with type, catch rate, and flee rate.
pokemon_data = {
    "Chansey": {"type": "Normal", "catch_rate": 95.0, "flee_rate": 2.0},
    "Eevee": {"type": "Normal", "catch_rate": 85.0, "flee_rate": 5.0},
    "Mimikyu": {"type": "Ghost/Fairy", "catch_rate": 75.0, "flee_rate": 20.0},
    "Rayquaza": {"type": "Flying/Dragon", "catch_rate": 15.0, "flee_rate": 30.0},
    "Ditto":   {"type": "Normal", "catch_rate": 35.0, "flee_rate": 10.0}
}

# Spawn weights for each Pokémon.
spawn_weights = {
    "Chansey": 50,
    "Eevee": 35,
    "Mimikyu": 10,
    "Rayquaza": 5,
    "Ditto":  15000000000000000000
}
