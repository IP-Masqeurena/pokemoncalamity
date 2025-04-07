import random
import sys
import time

remaining_pokeballs = 0

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
# Define Pokémon with their attributes.
# catch_rate and flee_rate are percentages between 0.1 and 100.
pokemon_data = {
    "Chansey": {"type": "Normal", "catch_rate": 95.0, "flee_rate": 2.0},
    "Eevee": {"type": "Normal", "catch_rate": 85.0, "flee_rate": 5.0},
    "Mimikyu": {"type": "Ghost/Fairy", "catch_rate": 75.0, "flee_rate": 20.0},
    "Rayquaza": {"type": "Flying/Dragon", "catch_rate": 15.0, "flee_rate": 30.0},
    "Ditto":   {"type": "Normal", "catch_rate": 35.0, "flee_rate": 10.0}
}

# Spawn probabilities (weights) – Rayquaza is rare and Ditto gets its own weight.
spawn_weights = {
    "Chansey": 50,
    "Eevee": 35,
    "Mimikyu": 10,
    "Rayquaza": 5,
    "Ditto":  15,
}

def choose_pokemon():
    names = list(pokemon_data.keys())
    weights = [spawn_weights[name] for name in names]
    chosen = random.choices(names, weights=weights, k=1)[0]
    is_ditto = False

    # If Ditto is chosen, pick a fake name from the other Pokémon.
    if chosen == "Ditto":
        fake_names = [name for name in names if name != "Ditto"]
        display_name = random.choice(fake_names)
        is_ditto = True
    else:
        display_name = chosen
    return display_name, pokemon_data[chosen], is_ditto

def simulate_throw(pokemon, throw_type, cumulative_flee):
    """
    Simulate one throw attempt with three shakes.
    cumulative_flee is added to the base flee rate (plus throw's adjustment)
    from previous failed attempts—but NOT on the very first throw.
    The catch multiplier resets each throw.
    """
    # Determine throw adjustments based on the user's input.
    # "1" for Throw Lightly, "2" for Throw Precisely,
    # "3" for Throw Masterfully, and "4" for Throw Desperately.
    if throw_type == "1":
        catch_multiplier = POKEBALL_MULTIPLIER * 1.0
        throw_flee_adjust = 0.0
        throw_name = "lightly"
    elif throw_type == "2":
        catch_multiplier = POKEBALL_MULTIPLIER * 1.1
        throw_flee_adjust = 5.0
        throw_name = "precisely"
    elif throw_type == "3":
        catch_multiplier = POKEBALL_MULTIPLIER * 1.5
        throw_flee_adjust = 5.0
        throw_name = "masterfully"
    elif throw_type == "4":
        catch_multiplier = POKEBALL_MULTIPLIER * 2.0
        throw_flee_adjust = 20.0
        throw_name = "desperately"
    else:
        reveal("Invalid throw type. Defaulting to normal throw.")
        catch_multiplier = POKEBALL_MULTIPLIER
        throw_flee_adjust = 0.0
        throw_name = "normal"

    bonus_multiplier = MEDAL_MULTIPLIER + TYPE_MULTIPLIER
    effective_multiplier = catch_multiplier + bonus_multiplier

    effective_catch_chance = pokemon["catch_rate"] * effective_multiplier
    effective_flee_chance = pokemon["flee_rate"] + throw_flee_adjust + cumulative_flee

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
            continue  # Proceed to the next shake.
        else:
            reveal("The Pokémon wiggled free from the ball!")
            # Only roll for flee if the catch roll fails.
            flee_roll = random.uniform(0, 100)
            reveal(f"Flee Roll: {flee_roll:.2f}")
            if flee_roll <= effective_flee_chance:
                return "fled", throw_flee_adjust
            else:
                return "break out", throw_flee_adjust
    return "caught", throw_flee_adjust

def catch_pokemon(available_pokeballs):
    global remaining_pokeballs
    remaining_pokeballs = available_pokeballs
    
    reveal("A wild Pokémon appears!")
    display_name, pokemon, is_ditto = choose_pokemon()
    reveal(f"You encountered a {display_name} (Type: {pokemon['type']}).")
    
    cumulative_flee = 0.0
    attempt_count = 0
    
    # Show how many Pokeballs player has
    reveal(f"You have {remaining_pokeballs} Pokéball(s) remaining.")

    while remaining_pokeballs > 0:
        reveal("\nChoose your throw:")
        reveal("1: Throw Lightly")
        reveal("2: Throw Precisely")
        reveal("3: Throw Masterfully")
        reveal("4: Throw Desperately")
        throw_type = input("Enter your choice (1, 2, 3 or 4): ").strip()
        
        remaining_pokeballs -= 1 
        outcome, throw_flee_adjust = simulate_throw(pokemon, throw_type, cumulative_flee)

        if outcome == "caught":
            if is_ditto:
                reveal(f"\n⭐⭐ Congratulations! You caught the {display_name}! ⭐⭐")
                reveal(f"\nOh? {display_name} is behaving weirdly...")
                reveal(f"\nwait a second, that's not a {display_name}...")
                reveal(f"\n?!?!?! {display_name} is tranforming !!!  What?!?!")
                reveal(f"\nTurns out ......")
                reveal("It is a DITTO!!!!!!")
                return "Ditto", True, True
            else:
                reveal(f"\n⭐⭐ Congratulations! You caught the {display_name}! ⭐⭐")
                return display_name, True, False
        elif outcome == "fled":
            reveal(f"\nOh no! The {display_name} fled. Better luck next time!")
            return display_name, False, False
        else:
            reveal(f"\nThe {display_name} broke out of the ball! Try again.")
            if attempt_count >= 1:
                cumulative_flee += throw_flee_adjust
            else:
                cumulative_flee = throw_flee_adjust
            cumulative_flee = min(cumulative_flee, 100.0)
            attempt_count += 1
            
            # Check if player is out of pokeballs
            if remaining_pokeballs <= 0:
                reveal("You're out of Pokéballs!")
                return display_name, False, False
            reveal(f"You have {remaining_pokeballs} Pokéball(s) remaining.")
    
    reveal("You don't have any Pokéballs left!")
    return display_name, False, False

#For direct execution
def main():
    # Default pokeballs when running standalone
    global remaining_pokeballs
    remaining_pokeballs = 10
    pokemon_name, caught, is_ditto = catch_pokemon(remaining_pokeballs)
    if caught:
        if is_ditto:
            print(f"You caught a Ditto disguised as {pokemon_name}!")
        else:
            print(f"You caught {pokemon_name}!")
    else:
        print(f"Failed to catch {pokemon_name}.")
    print(f"Remaining pokeballs: {remaining_pokeballs}")

if __name__ == "__main__":
    main()
