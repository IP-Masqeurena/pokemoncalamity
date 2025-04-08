import random
import sys
import time

def reveal(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Global multipliers and Pokémon data.
POKEBALL_MULTIPLIER = 1.0
MEDAL_MULTIPLIER = 1.0
TYPE_MULTIPLIER = 1.0

pokemon_data = {
    "Chansey": {"type": "Normal", "catch_rate": 95.0, "flee_rate": 2.0},
    "Eevee": {"type": "Normal", "catch_rate": 85.0, "flee_rate": 5.0},
    "Mimikyu": {"type": "Ghost/Fairy", "catch_rate": 75.0, "flee_rate": 20.0},
    "Rayquaza": {"type": "Flying/Dragon", "catch_rate": 15.0, "flee_rate": 30.0},
    "Ditto":   {"type": "Normal", "catch_rate": 35.0, "flee_rate": 10.0}
}

# Spawn probabilities (weights). Note that Ditto has a huge weight;
# if chosen Ditto will be replaced by a fake name from the other Pokémon.
spawn_weights = {
    "Chansey": 50,
    "Eevee": 30,
    "Mimikyu": 10,
    "Rayquaza": 1,
    "Ditto":  9
}

class Player:
    def __init__(self, filename="sf.txt"):
        self.filename = filename
        self.name = "Player"
        self.ID = None          # Will be a 5-digit string
        self.pokeballs = 10     # starting pokéballs (default)
        self.pokemons = {}      # Example: {"Chansey": 1, "Pikachu": 2}
        self.bag = {}           # Bag items if needed in the future.
        self.load_profile()

    def encode_number(self, number):
        """Encodes a number using a simple substitution cipher."""
        ENCODE_MAP = ['7', '0', '9', '8', '6', '2', '5', '3', '1', '4']
        return ''.join(ENCODE_MAP[int(d)] for d in str(number))

    def load_profile(self):
        """Loads player data from a save file. If the file doesn't exist, create one with default data."""
        try:
            with open(self.filename, "r") as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                if not line or ": " not in line:
                    continue
                key, value = line.split(": ", 1)
                if key.lower() == "name":
                    self.name = value
                elif key.lower() == "id":
                    self.ID = value
                elif key.lower() == "pokeballs":
                    self.pokeballs = int(value)
                elif key.lower() == "vanguard":
                    # Skipping verification for now.
                    pass
                else:
                    # Treat any other key as a Pokémon caught.
                    self.pokemons[key] = int(value)
        except Exception:
            # Save default profile if file does not exist or is unreadable.
            self.name = "Player"
            self.ID = str(random.randint(10000, 99999))
            self.pokeballs = 10
            self.pokemons = {"Pikachu": 1}  # Starter Pokémon.
            self.save_profile()

    def save_profile(self):
        """Saves player data back to the save file."""
        verification = self.encode_number(self.pokeballs)
        with open(self.filename, "w") as f:
            f.write("Name: " + self.name + "\n")
            if self.ID is None:
                self.ID = str(random.randint(10000, 99999))
            f.write("ID: " + self.ID + "\n")
            f.write("Pokeballs: " + str(self.pokeballs) + "\n")
            for name, count in self.pokemons.items():
                f.write(name + ": " + str(count) + "\n")
            f.write("Vanguard: " + verification + "\n")

    def add_pokemon(self, pokemon_name, count=1):
        """Records that the player caught a Pokémon."""
        self.pokemons[pokemon_name] = self.pokemons.get(pokemon_name, 0) + count
        self.save_profile()

class Game:
    def __init__(self):
        self.player = Player()

    def greet(self):
        reveal("=== Pokémon Terminal GO : Tester Version ===", 0.05)
        time.sleep(3)
        disclaimer = " This Project is Not Open Source, and is not intended to be used for any commercial purposes. "
        reveal(disclaimer, 0.05)

    def show_menu(self):
        print("========================")
        reveal("\nMain Menu:\n", 0.02)
        reveal("1. Profile", 0.02)
        reveal("2. Worlds", 0.02)
        reveal("3. Pokémon List", 0.02)
        reveal("4. Bag", 0.02)
        reveal("5. Shop", 0.02)
        reveal("6. Redeem", 0.02)
        reveal("7. Quit\n", 0.02)
        print("========================")

    def sub_menu(self):
        print("\n--- Sub Menu ---")
        print("1. Back to Main Menu")
        print("2. Quit")
        option = input("Select an option (1-2): ").strip()
        if option == "1":
            return  # Return to main loop.
        elif option == "2":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid selection, returning to Main Menu.")
            return

    def profile(self):
        print("=== Profile ===")
        print("Name:", self.player.name)
        print("ID:", self.player.ID)
        print("Pokémons:")
        if self.player.pokemons:
            for name, count in self.player.pokemons.items():
                print(f"{name} x{count}")
        else:
            print("None")
        print()

    def worlds(self):
        print("=== Worlds ===")
        reveal('\033[31m1. Aeos\033[0m')
        reveal('\033[38;5;137m2. Kanto\033[0m')
        reveal('\033[38;5;117m3. Johto\033[0m')
        reveal("4. Back to Main Menu", 0.02)
        world_choice = input("Choose a world (1-4): ").strip()
        if world_choice == "1":
            self.adventure_world("Aeos")
        elif world_choice == "2":
            self.adventure_world("Kanto")
        elif world_choice == "3":
            self.adventure_world("Johto")
        elif world_choice == "4":
            return
        else:
            print("Invalid selection.")
        # After finishing with a world, the main menu will be displayed again.

    def adventure_world(self, world):
        print(f"=== {world} Adventures ===")
        if world == "Aeos":
            reveal("1. Moonway Town", 0.02)
            reveal("2. Revolver City", 0.02)
        elif world == "Kanto":
            reveal("1. LittleRoot", 0.02)
            reveal("2. Viridian", 0.02)
        elif world == "Johto":
            reveal("1. GoldenRod", 0.02)
            reveal("2. Mahogany", 0.02)
        reveal("3. Back to Worlds", 0.02)
        city_choice = input("Choose a city (1-3): ").strip()
        if city_choice in ["1", "2"]:
            # Instead of a placeholder message, start the wild encounter.
            self.wild_encounter()
        elif city_choice == "3":
            return  # Back to Worlds menu.
        else:
            print("Invalid selection, returning to Worlds.")
        print()

    def pokemon_list(self):
        print("=== Pokémon List ===")
        if self.player.pokemons:
            for name, count in self.player.pokemons.items():
                print(f"{name} x{count}")
        else:
            print("No Pokémon caught yet!")
        print()

    def bag(self):
        print("=== Bag ===")
        print("Pokeballs:", self.player.pokeballs)
        print()

    def shop(self):
        print("=== Shop ===")
        add = input("Enter number of Pokeballs to add: ").strip()
        if add.isdigit():
            add = int(add)
            self.player.pokeballs += add
            self.player.save_profile()
            print(f"{add} Pokeballs added. Total now: {self.player.pokeballs}")
        else:
            print("Invalid number.")
        print()

    def redeem(self):
        print("=== Redeem Code ===")
        code = input("Enter redeem code: ").strip()
        if code == "CMDGO":
            self.player.pokeballs += 1000
            self.player.save_profile()
            print("Redeem successful! 1000 Pokeballs added.")
        else:
            print("Invalid code.")
        print()

    # --- Wild Encounter Functions ---

    def choose_pokemon(self):
        """Randomly select a wild Pokémon using spawn weights.
        If Ditto is chosen, a fake name from another Pokémon is used for display."""
        names = list(pokemon_data.keys())
        weights = [spawn_weights[name] for name in names]
        chosen = random.choices(names, weights=weights, k=1)[0]
        is_ditto = False
        if chosen == "Ditto":
            fake_names = [name for name in names if name != "Ditto"]
            display_name = random.choice(fake_names)
            is_ditto = True
        else:
            display_name = chosen
        return display_name, pokemon_data[chosen], is_ditto

    def simulate_throw(self, pokemon, throw_type, cumulative_flee):
        """Simulate one throw attempt. Deducts one Pokéball per throw.
        
        Returns a tuple:
            (outcome, throw_flee_adjust)
        outcome can be:
            - "caught" : Pokémon caught.
            - "fled"   : Pokémon fled.
            - "break out" : Pokémon breaks out, try again.
            - "no_balls"  : No Pokéballs left.
        """
        # Check if player has any Pokéballs left.
        if self.player.pokeballs <= 0:
            reveal("You have no Pokéballs left! The encounter ends.")
            return "no_balls", 0.0

        # Deduct one Pokéball per throw.
        self.player.pokeballs -= 1
        self.player.save_profile()

        # Determine throw adjustments.
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

    def wild_encounter(self):
        """Handles a wild Pokémon encounter. The encounter continues until the Pokémon is
        either caught or flees. After the encounter ends, the player is prompted whether to explore more."""
        exploring = True
        while exploring:
            reveal("A wild Pokémon appears!")
            display_name, pokemon, is_ditto = self.choose_pokemon()
            reveal(f"You encountered a {display_name} (Type: {pokemon['type']}).")

            cumulative_flee = 0.0
            attempt_count = 0

            while True:
                # Check if the player still has any Pokéballs.
                if self.player.pokeballs <= 0:
                    reveal("You have run out of Pokéballs!")
                    break

                reveal("\nChoose your throw:")
                reveal("1: Throw Lightly")
                reveal("2: Throw Precisely")
                reveal("3: Throw Masterfully")
                reveal("4: Throw Desperately")
                throw_type = input("Enter your choice (1, 2, 3, or 4): ").strip()
                outcome, throw_flee_adjust = self.simulate_throw(pokemon, throw_type, cumulative_flee)
                if outcome == "no_balls":
                    break  # End encounter if no Pokéballs.

                if outcome == "caught":
                    # Special handling for Ditto.
                    if is_ditto:
                        reveal(f"\n⭐⭐ Congratulations! You caught the {display_name}! ⭐⭐")
                        reveal("\nOh? Something feels off...")
                        reveal("\nWait a second... That's not a " + display_name + "...")
                        reveal("\n?!?!?! " + display_name + " is transforming!!!")
                        reveal("\nTurns out... It's a DITTO!!!!!!")
                    else:
                        reveal(f"\n⭐⭐ Congratulations! You caught the {display_name}! ⭐⭐")
                    # Register the catch.
                    self.player.add_pokemon(display_name)
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

            # Ask if the user wants to explore more wild encounters.
            choice = input("\nWould you like to explore more? (y/n): ").strip().lower()
            if choice != "y":
                exploring = False
                reveal("Returning to the main menu...")
                time.sleep(1)
                break

    def run(self):
        self.greet()
        while True:
            self.show_menu()
            choice = input("Select an option (1-7): ").strip()
            print()
            if choice == "1":
                self.profile()
                self.sub_menu()
            elif choice == "2":
                self.worlds()  # Worlds menu now leads to wild encounters.
            elif choice == "3":
                self.pokemon_list()
                self.sub_menu()
            elif choice == "4":
                self.bag()
                self.sub_menu()
            elif choice == "5":
                self.shop()
                self.sub_menu()
            elif choice == "6":
                self.redeem()
                self.sub_menu()
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid selection. Please choose again.")
            print()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
