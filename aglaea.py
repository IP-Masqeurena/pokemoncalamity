# main.py
import random
import sys
import time
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
        self.ID = None          # Will be a 5-digit string
        self.pokeballs = 10     # Starting pokéballs
        self.pokemons = {}      # Format: {"Chansey": 1, "Pikachu": 2}
        self.bag = {}           # For future bag items.
        self.load_profile()

    def encode_number(self, number):
        """Encodes a number using a simple substitution cipher."""
        ENCODE_MAP = ['7', '0', '9', '8', '6', '2', '5', '3', '1', '4']
        return ''.join(ENCODE_MAP[int(d)] for d in str(number))

    def load_profile(self):
        """Loads player data from a save file. Creates one with defaults if not found."""
        try:
            with open(self.filename, "r") as f:
                lines = f.readlines()
            # Parse lines in "Key: Value" format.
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
                    # Any other key is assumed to be a caught Pokémon.
                    self.pokemons[key] = int(value)
        except Exception:
            # Create default profile if file cannot be read.
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
        if city_choice in ["1", "2"]:
            # Start a wild encounter (calling our catch process).
            wild_encounter(self.player)
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
