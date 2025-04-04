import os
import time
import math

# Your detailed bush art as a list of strings.
bush = [
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡇⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡄",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⣷⠀⠀⠀⠀⡄⠀⠀⢸⣦⠀⠀⠀⠀⠀⠀⠀⠀⣠⡶⣾⡿⠋",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⡿⠀⢹⠀⢀⣴⡾⢻⡆⠀⢸⡿⣆⠀⠀⢀⣠⢀⣴⠞⣩⡾⣁⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⢦⣄⢸⡇⠀⢸⣶⢿⡿⠀⡌⠳⠀⣼⠇⣿⢠⡼⣿⣿⡟⠁⢠⣟⣥⣼⡿⠃",
    "⠀⠀⠀⠀⠀⠀⠀⠀⢶⣦⣌⣷⠙⢿⡇⠀⢸⠇⣿⣠⡾⠻⡕⣴⡏⠀⣽⠏⠀⣿⠋⠀⠀⣿⡟⢩⡟⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣄⠙⡇⠀⠀⠀⠈⠀⠹⠏⠀⠀⠙⠟⠀⠀⠀⠀⠀⠉⠀⠀⠀⠸⠷⣾⠁⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
]

# Parameters to control the swaying effect
amplitude = 2    # Maximum horizontal offset
frequency = 2    # How fast the wind oscillates

try:
    while True:
        # Use current time as a basis for the sine wave.
        t = time.time()
        os.system('cls' if os.name == 'nt' else 'clear')
        for i, line in enumerate(bush):
            # Create a phase shift for each line to simulate staggered movement.
            phase = i * math.pi / 6  
            # Calculate a small horizontal offset.
            offset = int(amplitude * math.sin(frequency * t + phase))
            
            if offset > 0:
                # Shift right by adding spaces.
                print(" " * offset + line)
            elif offset < 0:
                # Shift left by removing characters from the start.
                removal = abs(offset)
                print(line[removal:] if len(line) > removal else line)
            else:
                print(line)
        time.sleep(0.01)  # Adjust sleep for smoother or faster animation
except KeyboardInterrupt:
    print("\nAnimation stopped.")
