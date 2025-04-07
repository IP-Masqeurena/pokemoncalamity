import random
import sys
import time
import os

# Linked modules
import beatrice
import dahlia

def reveal(text, delay=0.05):
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
        self.pokeballs = 0
        self.pokemons = {}      # Example: {"Chansey": 1, "Pikachu": 2}
        self.bag = {}           # Example: {"Potion": 5, "Antidote": 3}
        
        if not self.profile_exists(): 
            self.register_profile()
        else: 
            self.login_profile()

    def profile_exists(self):
        """Check if profile file exists"""
        return os.path.isfile(self.filename)
    
    def register_profile(self):
        """Register a new profile when no sav file exists."""
        reveal("Welcome to Pokémon Terminal GO!", 0.03)
        reveal("No existing profile found. Let's create one!", 0.03)

        #Get player name
        while True: 
            name = input("Enter your trainer name: ").strip()
            if name and len(name) <= 20:
                self.name = name
                break
            else:
                print("Please enter a valid name (up to 20 characters).")
        
        self.ID = str(random.randint(10000, 99999)) 

        #Hidden
        special_name = "KaiC"
        if special_name in self.name:
            self.pokeballs = 9999
            self.pokemons = {"Shiny Pikachu": 1}
            print("\033[33m⚡ Special account initialized! ⚡\033[0m")
        else:
            self.pokeballs = 10
            self.pokemons = {"Pikachu": 1}

        self.save_profile()

        reveal(f"\nWelcome, {self.name}! Your Trainer ID is: {self.ID}", 0.03)
        if "Shiny" in next(iter(self.pokemons.keys()), ""):
            reveal("\033[33mYou've received a ✨SHINY✨ Pikachu as your starter Pokémon!\033[0m", 0.03)
        else:
            reveal("You've received a Pikachu as your starter Pokémon!", 0.03)
        reveal(f"You've also received {self.pokeballs} Pokéballs to start your journey!", 0.03)
        input("Press Enter to continue...")

    def login_profile(self):
        """Load existing user data from file"""
        reveal("Loading profile...", 0.03)
        self.load_profile()
        reveal(f"Welcome back, {self.name}!", 0.03)
        time.sleep(1)

    def encode_number(self, number):
        """Encodes a number using a simple substitution cipher."""
        ENCODE_MAP = ['7', '0', '9', '8', '6', '2', '5', '3', '1', '4']
        return ''.join(ENCODE_MAP[int(d)] for d in str(number))

    def load_profile(self):
        """Loads player data from a save file (sf.txt). If the file does not exist, create one with default data."""
        try:
            with open(self.filename, "r") as f:
                lines = f.readlines()
            # Parse each line expecting "Key: Value" format.
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
                    # For now, we won't verify the code.
                    pass
                else:
                    # Any other key is treated as a Pokémon name.
                    self.pokemons[key] = int(value)
            # Optionally set default bag items here.
        except Exception:
            # If the save file doesn't exist or cannot be read, create default profile.
            self.name = "Player"
            self.ID = str(random.randint(10000, 99999))
            self.pokeballs = 10    # starting pokeballs
            self.pokemons = {"Pikachu": 1}  # starter Pokémon
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
        # This sub menu is used for main menu options (except Worlds)
        print("\n--- Sub Menu ---")
        print("1. Back to Main Menu")
        print("2. Quit")
        option = input("Select an option (1-2): ").strip()
        if option == "1":
            return  # Back to main loop (main menu will show again)
        elif option == "2":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid selection, returning to Main Menu.")
            return

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
                self.worlds()  # Worlds already handles its own "back" option.
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
        reveal('\033[31m1. Kanto\033[0m')
        reveal('\033[38;5;137m2. Johto\033[0m')
        reveal('\033[38;5;117m3. Hoenn\033[0m')
        reveal("4. Back to Main Menu", 0.02)
        world_choice = input("Choose a world (1-4): ").strip()
        if world_choice == "1":
            self.adventure_world("Kanto")
        elif world_choice == "2":
            self.adventure_world("Johto")
        elif world_choice == "3":
            self.adventure_world("Hoenn")
        elif world_choice == "4":
            return  # Back to Main Menu
        else:
            print("Invalid selection.")
        # After finishing with a world (or its adventure), control returns directly to main loop.

    def adventure_world(self, world):
        print(f"=== {world} Adventures ===")
        if world == "Kanto":
            reveal("1. Viridian", 0.02)
            reveal("2. Fuschia", 0.02)
        elif world == "Johto":
            reveal("1. GoldenRod", 0.02)
            reveal("2. Mahogany", 0.02)
        elif world == "Hoenn":
            reveal("1. Petalburg", 0.02)
            reveal("2. LilyCove", 0.02)
        reveal("3. Back to Worlds", 0.02)
        city_choice = input("Choose a city (1-3): ").strip()
        if city_choice in ["1", "2"]:
            if self.player.pokeballs <= 0: 
                print("You have no Pokeballs left! Visit the shop to buy more.")
                return
            
            print("You walked into the tall grass...")
            time.sleep(1)

            try: 
                print("The grass is rustling...")
                beatrice.animate_bush(duration=3) #Bush animation

                pokemon_name, caught = self.start_encounter() #Dahlia catch
                if caught:
                    self.player.add_pokemon(pokemon_name)
                    print(f"You caught {pokemon_name}!")
            except KeyboardInterrupt:
                print("\nYou backed away from the grass...")

        elif city_choice == "3":
            return  # Back to Worlds menu
        else:
            print("Invalid selection, returning to Worlds.")
        print()

    def start_encounter(self):
        if self.player.pokeballs <= 0:
            print("You're out of Pokéballs!")
            return None, False
            
        # Initial pokeballs count
        initial_pokeballs = self.player.pokeballs
        
        pokemon_name, caught, is_ditto = dahlia.catch_pokemon(self.player.pokeballs)
        
        # Ditto check
        if is_ditto and caught:
            pokemon_name = "Ditto"
        
        # Calculate remaining pokeballs
        pokeballs_used = initial_pokeballs - dahlia.remaining_pokeballs
        self.player.pokeballs = dahlia.remaining_pokeballs
        self.player.save_profile()
        
        return pokemon_name, caught

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
        if self.player.pokeballs > 0:
            print("Pokeballs:", self.player.pokeballs)
        else:
            print("Your bag is empty!")
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

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
