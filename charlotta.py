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
    "Mimikyu": {"type": "Ghost/Fairy", "catch_rate": 25.0, "flee_rate": 30.0}
}

# Spawn probabilities (weights) - Mimikyu is the rarest.
spawn_weights = {
    "Chansey": 50,
    "Eevee": 40,
    "Mimikyu": 10
}

def choose_pokemon():
    names = list(pokemon_data.keys())
    weights = [spawn_weights[name] for name in names]
    chosen = random.choices(names, weights=weights, k=1)[0]
    return chosen, pokemon_data[chosen]

def simulate_throw(pokemon, throw_type):
    # Base catch multiplier (with medal bonus)
    catch_multiplier = POKEBALL_MULTIPLIER
    flee_rate_adjustment = 0.0

    if throw_type == "1":
        # Throw lightly: half the pokeball multiplier.
        catch_multiplier *= 0.5
        # No change to flee rate.
    elif throw_type == "2":
        # Reduce catch multiplier by 20%
        catch_multiplier *= 0.8
        # Increase flee rate by 5%
        flee_rate_adjustment = 5.0
    elif throw_type == "3":
        # Increase catch multiplier by 10%
        catch_multiplier *= 1.1
        # Increase flee rate by 20%
        flee_rate_adjustment = 20.0
    else:
        reveal("Invalid throw type. Defaulting to normal throw.")
    
    # Total effective catch multiplier includes the medal bonus.
    effective_multiplier = catch_multiplier + MEDAL_MULTIPLIER
    # Calculate effective catch chance and flee chance.
    effective_catch_chance = pokemon["catch_rate"] * effective_multiplier
    effective_flee_chance = pokemon["flee_rate"] + flee_rate_adjustment

    # Ensure probabilities do not exceed 100%
    effective_catch_chance = min(effective_catch_chance, 100.0)
    effective_flee_chance = min(effective_flee_chance, 100.0)

    # Roll for flee and catch
    flee_roll = random.uniform(0, 100)
    catch_roll = random.uniform(0, 100)

    reveal(f"\nThrow Type: {throw_type.capitalize()}")
    reveal(f"Effective Catch Chance: {effective_catch_chance:.2f}%")
    reveal(f"Effective Flee Chance: {effective_flee_chance:.2f}%")
    reveal(f"Flee Roll: {flee_roll:.2f} | Catch Roll: {catch_roll:.2f}")

    # Check outcomes: if Pokémon flees, it happens first.
    if flee_roll <= effective_flee_chance:
        return "fled"
    elif catch_roll <= effective_catch_chance:
        return "caught"
    else:
        return "break out"

def main():
    reveal("A wild Pokémon appears!")
    name, pokemon = choose_pokemon()
    reveal(f"You encountered a {name} (Type: {pokemon['type']}).")

    while True:
        throw_type = input("\nChoose your throw (lightly, precisely, desperately): ").strip()
        outcome = simulate_throw(pokemon, throw_type)

        if outcome == "caught":
            reveal(f"\nCongratulations! You caught the {name}!")
            break
        elif outcome == "fled":
            reveal(f"\nOh no! The {name} fled. Better luck next time!")
            break
        else:
            reveal(f"\nThe {name} broke out of the ball! Try again.")

if __name__ == "__main__":
    main()
