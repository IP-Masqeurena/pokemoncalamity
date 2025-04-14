# This file contains the Pokémon data and global constants.

# Base multipliers (note: these are now used only as a base; the actual bonus comes from medals)
POKEBALL_MULTIPLIER = 1.0
MEDAL_MULTIPLIER = 1.0
TYPE_MULTIPLIER = 1.0

# For each Pokémon, an "eva" field (evasion %) has been added.
area_data = {
    "Moonway Town": {
        "pokemon_data": {
            "Pokemon 1": {"type": "Normal", "catch_rate": 50.0, "flee_rate": 2.0, "eva": 5.0},
            "Pokemon 2": {"type": "Fire",   "catch_rate": 30.0, "flee_rate": 5.0, "eva": 15.0},
            "Pokemon 3": {"type": "Water",  "catch_rate": 20.0, "flee_rate": 3.0, "eva": 25.0}
        },
        "spawn_weights": {
            "Pokemon 1": 50,
            "Pokemon 2": 30,
            "Pokemon 3": 20
        }
    },
    "Revolver City": {
        "pokemon_data": {
            "Pokemon 1": {"type": "Electric", "catch_rate": 40.0, "flee_rate": 3.0, "eva": 10.0},
            "Pokemon 2": {"type": "Rock",     "catch_rate": 35.0, "flee_rate": 5.0, "eva": 20.0},
            "Pokemon 3": {"type": "Ghost",    "catch_rate": 25.0, "flee_rate": 10.0, "eva": 30.0}
        },
        "spawn_weights": {
            "Pokemon 1": 40,
            "Pokemon 2": 35,
            "Pokemon 3": 25
        }
    },
    "LittleRoot": {
        "pokemon_data": {
            "Pokemon 1": {"type": "Grass",    "catch_rate": 45.0, "flee_rate": 4.0, "eva": 10.0},
            "Pokemon 2": {"type": "Water",    "catch_rate": 35.0, "flee_rate": 5.0, "eva": 20.0},
            "Pokemon 3": {"type": "Bug",      "catch_rate": 20.0, "flee_rate": 8.0, "eva": 15.0}
        },
        "spawn_weights": {
            "Pokemon 1": 45,
            "Pokemon 2": 35,
            "Pokemon 3": 20
        }
    },
    "Viridian": {
        "pokemon_data": {
            "Pokemon 1": {"type": "Flying",   "catch_rate": 40.0, "flee_rate": 3.0, "eva": 15.0},
            "Pokemon 2": {"type": "Psychic",  "catch_rate": 35.0, "flee_rate": 5.0, "eva": 25.0},
            "Pokemon 3": {"type": "Fighting", "catch_rate": 25.0, "flee_rate": 10.0, "eva": 30.0}
        },
        "spawn_weights": {
            "Pokemon 1": 40,
            "Pokemon 2": 35,
            "Pokemon 3": 25
        }
    },
    "GoldenRod": {
        "pokemon_data": {
            "Pokemon 1": {"type": "Steel",    "catch_rate": 45.0, "flee_rate": 2.0, "eva": 10.0},
            "Pokemon 2": {"type": "Fairy",    "catch_rate": 35.0, "flee_rate": 5.0, "eva": 20.0},
            "Pokemon 3": {"type": "Dark",     "catch_rate": 20.0, "flee_rate": 10.0, "eva": 30.0}
        },
        "spawn_weights": {
            "Pokemon 1": 45,
            "Pokemon 2": 35,
            "Pokemon 3": 20
        }
    },
    "Mahogany": {
        "pokemon_data": {
            "Pokemon 1": {"type": "Ice",      "catch_rate": 40.0, "flee_rate": 4.0, "eva": 15.0},
            "Pokemon 2": {"type": "Dragon",   "catch_rate": 35.0, "flee_rate": 6.0, "eva": 25.0},
            "Pokemon 3": {"type": "Normal",   "catch_rate": 25.0, "flee_rate": 10.0, "eva": 5.0}
        },
        "spawn_weights": {
            "Pokemon 1": 40,
            "Pokemon 2": 35,
            "Pokemon 3": 25
        }
    }
}
