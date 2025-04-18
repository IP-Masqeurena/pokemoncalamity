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
MEDAL_MULTIPLIER = 1.0
TYPE_MULTIPLIER = 1.0  

# Define Pokémon with their attributes
# catch_rate and flee_rate are percentages between 0.1 and 100.
pokemon_data = {
    "Chansey": {"type": "Normal", "catch_rate": 95.0, "flee_rate": 2.0},
    "Eevee": {"type": "Normal", "catch_rate": 85.0, "flee_rate": 5.0},
    "Mimikyu": {"type": "Ghost/Fairy", "catch_rate": 75.0, "flee_rate": 20.0},
    "Rayquaza": {"type": "Flying/Dragon", "catch_rate": 1.0, "flee_rate": 30.0}
}

# Spawn probabilities (weights) - for example, Rayquaza is the rarest.
spawn_weights = {
    "Chansey": 50,
    "Eevee": 35,
    "Mimikyu": 10,
    "Rayquaza": 500000000000
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
    # "1" for Throw Lightly, "2" for Throw Precisely,
    # "3" for Throw Masterfully, and "4" for Throw Desperately.
    if throw_type == "1":
        # Lightly: base multiplier; no extra flee adjustment.
        catch_multiplier = POKEBALL_MULTIPLIER * 1.0
        throw_flee_adjust = 0.0
        throw_name = "lightly"
    elif throw_type == "2":
        # Precisely: slightly higher multiplier; add a moderate flee adjustment.
        catch_multiplier = POKEBALL_MULTIPLIER * 1.1
        throw_flee_adjust = 5.0
        throw_name = "precisely"
    elif throw_type == "3":
        # Masterfully: even higher multiplier; same flee adjustment as precisely.
        catch_multiplier = POKEBALL_MULTIPLIER * 1.5
        throw_flee_adjust = 5.0
        throw_name = "masterfully"
    elif throw_type == "4":
        # Desperately: highest multiplier; add a large extra flee adjustment.
        catch_multiplier = POKEBALL_MULTIPLIER * 2.0
        throw_flee_adjust = 20.0
        throw_name = "desperately"
    else:
        reveal("Invalid throw type. Defaulting to normal throw.")
        catch_multiplier = POKEBALL_MULTIPLIER
        throw_flee_adjust = 0.0
        throw_name = "normal"

    # Apply the medal bonus each throw (catch multiplier does not stack across throws).
    bonus_multiplier = MEDAL_MULTIPLIER + TYPE_MULTIPLIER
    effective_multiplier = catch_multiplier + bonus_multiplier

    # Calculate effective catch and flee chances.
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

        # First, roll for a catch.
        catch_roll = random.uniform(0, 100)
        reveal(f"Catch Roll: {catch_roll:.2f}")
        if catch_roll <= effective_catch_chance:
            reveal("The shake was secure!")
            continue  # Proceed to next shake.
        else:
            reveal("The Pokémon wiggled free from the ball!")
            # Only roll for flee if the catch roll fails.
            flee_roll = random.uniform(0, 100)
            reveal(f"Flee Roll: {flee_roll:.2f}")
            if flee_roll <= effective_flee_chance:
                # reveal("The pokemo")
                return "fled", throw_flee_adjust
            else:
                return "break out", throw_flee_adjust
    # If all three shakes produce a secure catch roll, then the Pokémon is caught.
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
                cumulative_flee = throw_flee_adjust
            cumulative_flee = min(cumulative_flee, 100.0)
            attempt_count += 1

if __name__ == "__main__":
    main()
