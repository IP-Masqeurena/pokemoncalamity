# catch.py
import random
import sys
import time
from gaia import area_data, POKEBALL_MULTIPLIER, MEDAL_MULTIPLIER, TYPE_MULTIPLIER

def reveal(text, delay=0.05):
    """Prints text with a typing effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def choose_pokemon(area_name):
    """Randomly selects a wild Pokémon using spawn weights.
    
    If Ditto is chosen, a fake name from another Pokémon is used for display.
    Returns a tuple (display_name, pokemon_stats, is_ditto).
    """
    area_info = area_data.get(area_name)
    if not area_info:
        reveal("Area data not found. Defaulting to first available area.")
        # Fallback: choose the first area in area_data.
        area_info = list(area_data.values())[0]

    pokemon_data_local = area_info["pokemon_data"]
    spawn_weights_local = area_info["spawn_weights"]

    names = list(pokemon_data_local.keys())
    weights = [spawn_weights_local[name] for name in names]
    chosen = random.choices(names, weights=weights, k=1)[0]
    
    # (Optional: add any Ditto check here if necessary)
    is_ditto = (chosen == "Ditto")
    display_name = chosen  # or use a fake name for Ditto if desired.
    
    return display_name, pokemon_data_local[chosen], is_ditto

def simulate_throw(player, pokemon, throw_type, cumulative_flee):
    """
    Simulates one throw attempt during a wild encounter.
    
    Deducts one Pokéball from the player's inventory. Returns a tuple:
      (outcome, throw_flee_adjust)
    where outcome is:
      - "caught"   : Pokémon caught
      - "fled"     : Pokémon fled
      - "break out": Pokémon breaks out (encounter continues)
      - "no_balls" : Player ran out of Pokéballs
    """
    # Check if the player has any Pokéballs left.
    if player.pokeballs <= 0:
        reveal("You have no Pokéballs left! The encounter ends.")
        return "no_balls", 0.0

    # Deduct one Pokéball per throw.
    player.pokeballs -= 1
    player.save_profile()

    # Determine throw adjustments and multipliers based on the throw type.
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

        # Roll for catch.
        catch_roll = random.uniform(0, 100)
        reveal(f"Catch Roll: {catch_roll:.2f}")
        if catch_roll <= effective_catch_chance:
            reveal("The shake was secure!")
            continue
        else:
            reveal("The Pokémon wiggled free from the ball!")
            # Roll for flee if catch fails.
            flee_roll = random.uniform(0, 100)
            reveal(f"Flee Roll: {flee_roll:.2f}")
            if flee_roll <= effective_flee_chance:
                return "fled", throw_flee_adjust
            else:
                return "break out", throw_flee_adjust
    return "caught", throw_flee_adjust

def wild_encounter(player, area_name):
    """
    Handles a wild Pokémon encounter. The encounter continues until the Pokémon
    is either caught or flees. After a catch or a flee, the player is asked if they want
    to explore more encounters.
    
    When caught, the Pokémon is registered to the player's profile.
    """
    exploring = True
    while exploring:
        reveal("A wild Pokémon appears!")
        display_name, pokemon, is_ditto = choose_pokemon(area_name)
        reveal(f"You encountered a {display_name} (Type: {pokemon['type']}).")

        cumulative_flee = 0.0
        attempt_count = 0

        # Encounter loop for the current wild Pokémon.
        while True:
            if player.pokeballs <= 0:
                reveal("You have run out of Pokéballs!")
                break

            reveal("\nChoose your throw:")
            reveal("1: Throw Lightly")
            reveal("2: Throw Precisely")
            reveal("3: Throw Masterfully")
            reveal("4: Throw Desperately")
            throw_type = input("Enter your choice (1, 2, 3, or 4): ").strip()
            outcome, throw_flee_adjust = simulate_throw(player, pokemon, throw_type, cumulative_flee)
            
            if outcome == "no_balls":
                break

            if outcome == "caught":
                if is_ditto:
                    reveal(f"\n⭐⭐ Congratulations! You caught the {display_name}! ⭐⭐")
                    reveal("\nOh? Something feels off...")
                    reveal("\nWait a second... That's not a " + display_name + "...")
                    reveal("\n?!?!?! " + display_name + " is transforming!!!")
                    reveal("\nTurns out... It's a DITTO!!!!!!")
                    # Assume Ditto’s type is Normal.
                    player.add_pokemon("Ditto", "Normal")
                else:
                    reveal(f"\n⭐⭐ Congratulations! You caught the {display_name}! ⭐⭐")
                    # Provide the actual type from the pokemon's data.
                    player.add_pokemon(display_name, pokemon["type"])
                break
            elif outcome == "fled":
                reveal(f"\nOh no! The {display_name} fled. Better luck next time!")
                break
            else:
                reveal(f"\nThe {display_name} broke out of the ball! Try again.")
                if attempt_count >= 1:
                    cumulative_flee += throw_flee_adjust
                else:
                    cumulative_flee = throw_flee_adjust
                cumulative_flee = min(cumulative_flee, 100.0)
                attempt_count += 1

        choice = input("\nWould you like to explore more? (y/n): ").strip().lower()
        if choice != "y":
            exploring = False
            reveal("Returning to the main menu...")
            time.sleep(1)
            break
