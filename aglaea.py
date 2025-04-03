import random
import sys , time , os

def reveal( text, delay=0.05):
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
        self.load_profile()


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
            # If bag is not stored, set some default items.
            self.bag = {"Potion": 5, "Antidote": 3}
        except Exception:
            # If the save file doesn't exist or cannot be read, create default profile.
            self.name = "Player"
            self.ID = str(random.randint(10000, 99999))
            self.pokeballs = 10    # starting pokeballs
            self.pokemons = {"Pikachu": 1}  # starter Pokémon
            self.bag = {"Potion": 5, "Antidote": 3}
            self.save_profile()

    def save_profile(self):
        """Saves player data back to the save file in the format:
           Name: <name>
           ID: <ID>
           Pokeballs: <pokeballs>
           [PokemonName: count] for each caught pokemon (if any)
           Vanguard: <verification>
        """
        verification = self.encode_number(self.pokeballs)
        with open(self.filename, "w") as f:
            f.write("Name: " + self.name + "\n")
            if self.ID is None:
                # Generate an ID if it wasn't set
                self.ID = str(random.randint(10000, 99999))
            f.write("ID: " + self.ID + "\n")
            f.write("Pokeballs: " + str(self.pokeballs) + "\n")
            for name, count in self.pokemons.items():
                f.write(name + ": " + str(count) + "\n")
            f.write("Vanguard: " + verification + "\n")

    def add_pokemon(self, pokemon_name, count=1):
        """Records that the player caught a Pokémon (or increases the count)."""
        self.pokemons[pokemon_name] = self.pokemons.get(pokemon_name, 0) + count
        self.save_profile()


class Game:
    def __init__(self):
        self.player = Player()

    def greet(self):
        print("=== Pokémon Terminal GO : Tester Version ===")
        time.sleep(3)
        # print("Disclaimer: let me put what ever i wan")
        # time.sleep(15)
        disclaimer = " This Project is Not Open Source, and is not intended to be used for any commercial purposes. " 
        for char in disclaimer:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)
        print()

    def show_menu(self):
        print("========================")
        reveal("\nMain Menu:\n",0.02)
        reveal("1. Profile",0.02)
        reveal("2. Adventure",0.02)
        reveal("3. Pokémon List",0.02)
        reveal("4. Bag",0.02)
        reveal("5. Shop",0.02)
        reveal("6. Redeem",0.02)
        reveal("7. Quit\n",0.02)
        print("========================")

    def run(self):
        self.greet()
        while True:
            self.show_menu()
            choice = input("Select an option (1-7): ").strip()
            print()
            if choice == "1":
                self.profile()
            elif choice == "2":
                self.adventure()
            elif choice == "3":
                self.pokemon_list()
            elif choice == "4":
                self.bag()
            elif choice == "5":
                self.shop()
            elif choice == "6":
                self.redeem()
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
        print("Pokeballs:", self.player.pokeballs)
        print("Pokémons:")
        if self.player.pokemons:
            for name, count in self.player.pokemons.items():
                print(f"{name} x{count}")
        else:
            print("None")
        print()

    def adventure(self):
        print("=== Adventure ===")
        print("Locations:")
        print("1. Forest")
        print("2. Stream")
        print("3. Cave")
        loc = input("Choose a location (1-3): ").strip()
        if loc in ["1", "2", "3"]:
            print("You ventured into the location... (feature coming soon)")
        else:
            print("Invalid location.")
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
        if self.player.bag:
            for item, quantity in self.player.bag.items():
                print(f"{item}: {quantity}")
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
