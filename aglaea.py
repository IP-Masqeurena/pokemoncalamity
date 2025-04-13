import random
import sys
import time
import os
from fluerdylis import wild_encounter

def reveal(text, delay=0.01):
    """Prints text with a typing effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class Player:
    def __init__(self, filename="sf.txt"):
        self.filename = filename
        self.name = "Player"
        self.ID = None
        self.pokeballs = 10
        self.pokemons = {}          # Pokémon caught: e.g., {"Pikachu": 1, ...}
        # New attributes for catches tracking and stats:
        self.total_catches = 0      # overall number of successful catches
        self.catches_by_type = {}   # e.g., {"Fire": 3, "Water": 2, ...}
        self.xp = 0                 # XP gained (1 XP per catch)
        self.level = 1              # starting level
        self.hp = 3                 # starting HP (level + 2)
        self.spd = 10               # starting SPD (10 at level 1, +1 per level)
        self.load_profile()

    def encode_number(self, number):
        """Encodes a number using a simple substitution cipher."""
        ENCODE_MAP = ['7', '0', '9', '8', '6', '2', '5', '3', '1', '4']
        return ''.join(ENCODE_MAP[int(d)] for d in str(number))

    def check_level_up(self):
        """Checks and applies level-up based on XP.
           Level thresholds: 
             level 1→2: 10 XP, level 2→3: 15 XP, level 3→4: 20 XP, etc.
           For every level up, increase level by 1 and recalc HP and SPD.
           HP is recalculated as (level + 2) and SPD as 10 + (level - 1).
        """
        threshold = 10 + (self.level - 1) * 5
        while self.xp >= threshold:
            self.xp -= threshold
            self.level += 1
            self.hp = self.level + 2
            self.spd = 10 + (self.level - 1)
            threshold = 10 + (self.level - 1) * 5

    def add_pokemon(self, pokemon_name, poke_type, count=1):
        """Records that the player caught a Pokémon and updates statistics.
           Awards 1 XP per catch, increments overall catches and type counts,
           then checks for level-up.
        """
        self.total_catches += count
        # Update catches by type:
        if poke_type in self.catches_by_type:
            self.catches_by_type[poke_type] += count
        else:
            self.catches_by_type[poke_type] = count
        # Update the Pokémon caught list:
        self.pokemons[pokemon_name] = self.pokemons.get(pokemon_name, 0) + count
        # Award 1 XP per catch and check for level-up:
        self.xp += 10
        self.check_level_up()
        self.save_profile()

    def load_profile(self):
        """
        Loads player data from the save file in a neat, sectioned format.
        
        Global:
          Name, ID, Pokeballs

        -- Player Stats --
          Level, XP, HP, SPD, Vanguard.

        -- Catches --
          Total Catches, then individual type counts.

        -- Pokemon Caught --
          Each Pokémon caught.
        """
        if not os.path.exists(self.filename):
            # File does not exist so create with defaults.
            self.ID = str(random.randint(10000, 99999))
            self.save_profile()
            return

        current_section = "global"
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    # Detect section headers.
                    if line.startswith("--"):
                        if "Player Stats" in line:
                            current_section = "stats"
                        elif "Catches" in line:
                            current_section = "catches"
                        elif "Pokemon Caught" in line:
                            current_section = "pokemons"
                        else:
                            current_section = ""
                        continue

                    if ": " in line:
                        key, value = line.split(": ", 1)
                        if current_section == "global":
                            if key == "Name":
                                self.name = value
                            elif key == "ID":
                                self.ID = value
                            elif key == "Pokeballs":
                                self.pokeballs = int(value)
                        elif current_section == "stats":
                            if key == "Level":
                                self.level = int(value)
                            elif key == "XP":
                                self.xp = int(value)
                            elif key == "HP":
                                self.hp = int(value)
                            elif key == "SPD":
                                self.spd = int(value)
                            # Vanguard is saved but not used here.
                        elif current_section == "catches":
                            if key == "Total Catches":
                                self.total_catches = int(value)
                            else:
                                # Here assume any key is a type name.
                                self.catches_by_type[key] = int(value)
                        elif current_section == "pokemons":
                            self.pokemons[key] = int(value)
        except Exception:
            # In case of error, reinitialize with defaults.
            self.name = "Player"
            self.ID = str(random.randint(10000, 99999))
            self.pokeballs = 10
            self.pokemons = {}
            self.total_catches = 0
            self.catches_by_type = {}
            self.xp = 0
            self.level = 1
            self.hp = 3
            self.spd = 10
            self.save_profile()

    def save_profile(self):
        """Saves player data into the save file, using a neat, sectioned format."""
        verification = self.encode_number(self.pokeballs)
        with open(self.filename, "w") as f:
            # Global section.
            f.write(f"Name: {self.name}\n")
            if self.ID is None:
                self.ID = str(random.randint(10000, 99999))
            f.write(f"ID: {self.ID}\n")
            f.write(f"Pokeballs: {self.pokeballs}\n\n")
            
            # Player Stats section (moved above the other sections).
            f.write("-- Player Stats --\n")
            f.write(f"Level: {self.level}\n")
            f.write(f"XP: {self.xp}\n")
            f.write(f"HP: {self.hp}\n")
            f.write(f"SPD: {self.spd}\n")
            f.write(f"Vanguard: {verification}\n\n")
            
            # Catches section.
            f.write("-- Catches --\n")
            f.write(f"Total Catches: {self.total_catches}\n")
            for poke_type, count in self.catches_by_type.items():
                f.write(f"{poke_type}: {count}\n")
            f.write("\n")
            
            # Pokemon Caught section.
            f.write("-- Pokemon Caught --\n")
            for name, count in self.pokemons.items():
                f.write(f"{name}: {count}\n")

class Game:
    def __init__(self):
        self.player = None

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
            return  # Back to main menu.
        elif option == "2":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid selection, returning to Main Menu.")

    def profile(self):
        print("=== Profile ===")
        print("Name:", self.player.name)
        print("ID:", self.player.ID)
        print("\nPokémons:")
        if self.player.pokemons:
            for name, count in self.player.pokemons.items():
                print(f"{name} x{count}")
        else:
            print("None")
        # Display additional stats.
        print("\n-- Stats --")
        print(f"Total Catches: {self.player.total_catches}")
        print("Catches by Type:")
        for ptype, count in self.player.catches_by_type.items():
            print(f"{ptype}: {count}")
        print(f"Level: {self.player.level}   XP: {self.player.xp}   HP: {self.player.hp}   SPD: {self.player.spd}")
        print()

    def worlds(self):
        print("=== Worlds ===")
        reveal('\033[31m1. Aeos\033[0m')
        reveal('\033[38;5;137m2. Kanto\033[0m')
        reveal('\033[38;5;117m3. Johto\033[0m')
        reveal("4. Back to Main Menu", 0.02)
        world_choice = input("Choose a world (1-4): ").strip()
        if world_choice in ["1", "2", "3"]:
            self.adventure_world(world_choice)
        elif world_choice == "4":
            return
        else:
            print("Invalid selection.")

    def adventure_world(self, world_choice):
        if world_choice == "1":
            world = "Aeos"
            print(f"=== {world} Adventures ===")
            reveal("1. Moonway Town", 0.02)
            reveal("2. Revolver City", 0.02)
        elif world_choice == "2":
            world = "Kanto"
            print(f"=== {world} Adventures ===")
            reveal("1. LittleRoot", 0.02)
            reveal("2. Viridian", 0.02)
        elif world_choice == "3":
            world = "Johto"
            print(f"=== {world} Adventures ===")
            reveal("1. GoldenRod", 0.02)
            reveal("2. Mahogany", 0.02)
        reveal("3. Back to Worlds", 0.02)
        city_choice = input("Choose a city (1-3): ").strip()
        
        # Standardized lookup: nested dictionary keyed by world.
        area_lookup = {
            "Aeos": {
                "1": "Moonway Town",
                "2": "Revolver City"
            },
            "Kanto": {
                "1": "LittleRoot",
                "2": "Viridian"
            },
            "Johto": {
                "1": "GoldenRod",
                "2": "Mahogany"
            }
        }
        
        if city_choice in area_lookup.get(world, {}):
            area_name = area_lookup[world][city_choice]
            wild_encounter(self.player, area_name)
        elif city_choice == "3":
            return
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
        add = input("Enter number of Pokéballs to add: ").strip()
        if add.isdigit():
            add = int(add)
            self.player.pokeballs += add
            self.player.save_profile()
            print(f"{add} Pokéballs added. Total now: {self.player.pokeballs}")
        else:
            print("Invalid number.")
        print()

    def redeem(self):
        print("=== Redeem Code ===")
        code = input("Enter redeem code: ").strip()
        if code == "CMDGO":
            self.player.pokeballs += 1000
            self.player.save_profile()
            print("Redeem successful! 1000 Pokéballs added.")
        else:
            print("Invalid code.")
        print()

    def run(self):
        self.greet()
        # Check if save file exists
        if not os.path.exists("sf.txt"):
            reveal("\nWelcome new Trainer!")
            while True:
                name = input("What is your name? ").strip()
                if name:
                    self.player = Player()
                    self.player.name = name
                    self.player.save_profile()
                    break
                else:
                    print("Please enter a valid name.")
        else:
            self.player = Player()
        while True:
            self.show_menu()
            choice = input("Select an option (1-7): ").strip()
            print()
            if choice == "1":
                self.profile()
                self.sub_menu()
            elif choice == "2":
                self.worlds()
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
