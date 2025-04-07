import random
import sys
import time

def reveal(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Define base multipliers
POKEBALL_MULTIPLIER = 1.0
MEDAL_MULTIPLIER = 0.1

# Define three Pokémon with their attributes
# catch_rate and flee_rate are percentages between 0.1 and 100.
pokemon_data = {
    "Chansey": {"type": "Normal", "catch_rate": 70.0, "flee_rate": 10.0},
    "Eevee": {"type": "Normal", "catch_rate": 50.0, "flee_rate": 20.0},
    "Mimikyu": {"type": "Ghost/Fairy", "catch_rate": 25.0, "flee_rate": 30.0},
    "Rayquaza": {"type": "Flying/Dragon", "catch_rate": 15, "flee_rate": 60.0}
}

# Spawn probabilities (weights) - Mimikyu is the rarest.
spawn_weights = {
    "Chansey": 50,
    "Eevee": 35,
    "Mimikyu": 10,
    "Rayquaza": 5
}

def choose_pokemon():
    names = list(pokemon_data.keys())
    weights = [spawn_weights[name] for name in names]
    chosen = random.choices(names, weights=weights, k=1)[0]
    return chosen, pokemon_data[chosen]

def simulate_throw(pokemon, throw_type, cumulative_flee):
    """
    Simulate one throw attempt with three shakes.
    The flee rate stacks: cumulative_flee is added to the base flee rate and this throw's adjustment.
    The catch multiplier resets each throw.
    """
    # Determine throw adjustments:
    # For throw_type, user enters "1" for lightly, "2" for precisely, "3" for desperately.
    if throw_type == "1":
        # Lightly: half the pokeball multiplier; no extra flee adjustment.
        catch_multiplier = POKEBALL_MULTIPLIER * 1
        throw_flee_adjust = 0.0
        throw_name = "lightly"
    elif throw_type == "2":
        # Precisely: reduce catch multiplier by 20%; add 5% extra flee rate.
        catch_multiplier = POKEBALL_MULTIPLIER * 1.1
        throw_flee_adjust = 5.0
        throw_name = "precisely"
    elif throw_type == "3":
        # Desperately: increase catch multiplier by 10%; add 20% extra flee rate.
        catch_multiplier = POKEBALL_MULTIPLIER * 2.0
        throw_flee_adjust = 20.0
        throw_name = "desperately"
    else:
        reveal("Invalid throw type. Defaulting to normal throw.")
        catch_multiplier = POKEBALL_MULTIPLIER
        throw_flee_adjust = 0.0
        throw_name = "normal"

    # The catch multiplier resets on each throw; add the medal bonus.
    effective_multiplier = catch_multiplier + MEDAL_MULTIPLIER
    # Calculate effective catch and flee chances.
    effective_catch_chance = pokemon["catch_rate"] * effective_multiplier
    effective_flee_chance = pokemon["flee_rate"] + throw_flee_adjust + cumulative_flee

    # Cap both values at 100%
    effective_catch_chance = min(effective_catch_chance, 100.0)
    effective_flee_chance = min(effective_flee_chance, 100.0)

    reveal(f"\nYou threw the ball {throw_name}.")
    reveal(f"Effective Catch Chance: {effective_catch_chance:.2f}%")
    reveal(f"Effective Flee Chance: {effective_flee_chance:.2f}%")

    # Simulate three shakes.
    for i in range(1, 4):
        shake_label = ""
        if i == 1:
            shake_label = "Shake ONCE"
        elif i == 2:
            shake_label = "Shake TWICE"
        elif i == 3:
            shake_label = "SHAKE THRICE"
        reveal(f"\n{shake_label}...")
        # For each shake, roll a random number.
        roll = random.uniform(0, 100)
        reveal(f"Roll: {roll:.2f}")
        # Check for flee first.
        if roll <= effective_flee_chance:
            reveal("Oh no! It triggered a flee!")
            # Return outcome along with the throw's flee adjustment (to be added if throw fails)
            return "fled", throw_flee_adjust
        # Next, check if the shake is secure.
        elif roll > effective_catch_chance:
            reveal("The Pokémon wiggled free from the ball!")
            return "break out", throw_flee_adjust
        else:
            reveal("The shake was secure!")
    # If all three shakes are secure:
    return "caught", throw_flee_adjust

def main():
    reveal("A wild Pokémon appears!")
    name, pokemon = choose_pokemon()
    reveal(f"You encountered a {name} (Type: {pokemon['type']}).")
    
    # cumulative_flee tracks the stacked flee chance from previous failed attempts.
    cumulative_flee = 0.0

    while True:
        reveal("\nChoose your throw:")
        reveal("1: Throw Lightly")
        reveal("2: Throw Precisely")
        reveal("3: Throw Desperately")
        throw_type = input("Enter your choice (1, 2, or 3): ").strip()
        outcome, throw_flee_adjust = simulate_throw(pokemon, throw_type, cumulative_flee)

        if outcome == "caught":
            reveal(f"\nCongratulations! You caught the {name}!")
            break
        elif outcome == "fled":
            reveal(f"\nOh no! The {name} fled. Better luck next time!")
            break
        else:
            # The Pokémon broke out of the ball.
            reveal(f"\nThe {name} broke out of the ball! Try again.")
            # Increase cumulative flee chance only if the throw adjustment was non-zero.
            cumulative_flee += throw_flee_adjust
            # Cap cumulative flee at 100.
            cumulative_flee = min(cumulative_flee, 100.0)

if __name__ == "__main__":
    main()
