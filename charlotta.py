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
MEDAL_MULTIPLIER = 5.0

# Define Pokémon with their attributes
# catch_rate and flee_rate are percentages between 0.1 and 100.
pokemon_data = {
    "Chansey": {"type": "Normal", "catch_rate": 99.0, "flee_rate": 1.0},
    "Eevee": {"type": "Normal", "catch_rate": 50.0, "flee_rate": 20.0},
    "Mimikyu": {"type": "Ghost/Fairy", "catch_rate": 25.0, "flee_rate": 30.0},
    "Rayquaza": {"type": "Flying/Dragon", "catch_rate": 15.0, "flee_rate": 60.0}
}

# Spawn probabilities (weights) - for example, Rayquaza is the rarest.
spawn_weights = {
    "Chansey": 50,
    "Eevee": 35,
    "Mimikyu": 10,
    "Rayquaza": 50000000000
}

def choose_pokemon():
    names = list(pokemon_data.keys())
    weights = [spawn_weights[name] for name in names]
    chosen = random.choices(names, weights=weights, k=1)[0]
    return chosen, pokemon_data[chosen]

def simulate_throw(pokemon, throw_type, cumulative_flee):
    """
    Simulate one throw attempt with three shakes.
    cumulative_flee is added to the base flee rate (plus throw's adjustment)
    from previous failed attempts—but NOT on the very first throw.
    The catch multiplier resets each throw.
    """
    # Determine throw adjustments based on the user's input.
    # For throw_type, the user enters:
    # "1" for Throw Lightly, "2" for Throw Precisely, "3" for Throw Desperately.
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
        # Precisely: reduce catch multiplier by 20%; add 5% extra flee rate.
        catch_multiplier = POKEBALL_MULTIPLIER * 1.5
        throw_flee_adjust = 5.0
        throw_name = "masterfully"
    elif throw_type == "4":
        # Desperately: increase catch multiplier by 10%; add 20% extra flee rate.
        catch_multiplier = POKEBALL_MULTIPLIER * 2.0
        throw_flee_adjust = 20.0
        throw_name = "desperately"
    else:
        reveal("Invalid throw type. Defaulting to normal throw.")
        catch_multiplier = POKEBALL_MULTIPLIER
        throw_flee_adjust = 0.0
        throw_name = "normal"

    # Apply the medal bonus each throw (catch multiplier does not stack across throws).
    effective_multiplier = catch_multiplier + MEDAL_MULTIPLIER

    # Calculate effective catch and flee chances.
    # The effective flee chance uses the Pokémon's base flee rate plus the throw's adjustment and the cumulative flee from previous attempts.
    effective_catch_chance = pokemon["catch_rate"] * effective_multiplier
    effective_flee_chance = pokemon["flee_rate"] + throw_flee_adjust + cumulative_flee

    # Cap probabilities at 100%.
    effective_catch_chance = min(effective_catch_chance, 100.0)
    effective_flee_chance = min(effective_flee_chance, 100.0)

    reveal(f"\nYou threw the ball {throw_name}.")
    reveal(f"Effective Catch Chance: {effective_catch_chance:.2f}%")
    reveal(f"Effective Flee Chance: {effective_flee_chance:.2f}%")

    # Simulate three shakes.
    for i in range(1, 4):
        if i == 1:
            shake_label = "Shake ONCE"
        elif i == 2:
            shake_label = "Shake TWICE"
        elif i == 3:
            shake_label = "SHAKE THRICE"
        reveal(f"\n{shake_label}...")
        # Each shake has its own random roll.
        roll = random.uniform(0, 100)
        reveal(f"Roll: {roll:.2f}")
        # Check for flee first.
        if roll <= effective_flee_chance:
            reveal("Oh no! It triggered a flee!")
            return "fled", throw_flee_adjust
        # Then check if the shake is secure (roll falls within catch chance).
        elif roll > effective_catch_chance:
            reveal("The Pokémon wiggled free from the ball!")
            return "break out", throw_flee_adjust
        else:
            reveal("The shake was secure!")
    # If all three shakes pass, the Pokémon is caught.
    return "caught", throw_flee_adjust

def main():
    reveal("A wild Pokémon appears!")
    name, pokemon = choose_pokemon()
    reveal(f"You encountered a {name} (Type: {pokemon['type']}).")
    
    # cumulative_flee tracks extra flee chance added from previous failed attempts.
    cumulative_flee = 0.0
    attempt_count = 0

    while True:
        reveal("\nChoose your throw:")
        reveal("1: Throw Lightly")
        reveal("2: Throw Precisely")
        reveal("3: Throw Masterfully")
        reveal("4: Throw Desperately")
        throw_type = input("Enter your choice (1, 2, 3 or 4): ").strip()
        outcome, throw_flee_adjust = simulate_throw(pokemon, throw_type, cumulative_flee)

        if outcome == "caught":
            reveal(f"\n⭐⭐ Congratulations! You caught the {name}! ⭐⭐")
            break
        elif outcome == "fled":
            reveal(f"\nOh no! The {name} fled. Better luck next time!")
            break
        else:
            # The Pokémon broke out of the ball.
            reveal(f"\nThe {name} broke out of the ball! Try again.")
            # Only update cumulative_flee after the first throw.
            if attempt_count >= 1:
                cumulative_flee += throw_flee_adjust
            else:
                # After the first failed attempt, set cumulative flee to the throw's adjustment.
                cumulative_flee = throw_flee_adjust
            # Cap cumulative flee at 100.
            cumulative_flee = min(cumulative_flee, 100.0)
            attempt_count += 1

if __name__ == "__main__":
    main()
