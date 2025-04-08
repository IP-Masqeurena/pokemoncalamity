import os
import time

# Cyclist ASCII art (use your provided art)
cyclist_art = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣾⡀⠻⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣾⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⠛⣛⣉⡀⠙⢿⣶⣤⣄⣀⣀⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣯⣿⣿⣿⣤⣤⣤⣭⣽⡟⠈⠙⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠏⢻⣿⣿⠟⠀⠀⠀⢠⡿⢻⣧⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣤⡶⠿⠛⠻⣾⣯⡀⢾⣿⣿⡆⠀⢀⡴⠋⢀⣤⣿⡿⠛⠿⢶⣤⡀⠀⠀
⠀⢀⣾⠁⠀⠀⢀⣾⠃⠈⢿⡄⠘⠿⠛⠰⠟⠁⢠⡿⠁⠈⣷⡀⠀⠀⠈⣷⡀⠀
⠀⢸⡇⠀⠀⠀⠾⠷⠶⠶⢾⣷⠆⠰⣶⠆⠀⠀⢸⠁⠀⠀⠘⠗⠀⠀⠀⢸⡇⠀
⠀⠘⣷⡀⠀⠀⠀⠀⠀⠀⣸⠃⠀⠀⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⢀⣾⠃
⠀⠀⠈⠻⣦⣀⣀⣀⣤⠾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠘⠷⣤⣀⣀⣀⣴⠟⠁⠀
⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉
"""

# Define the visible width (for drawing the cyclist and slicing the road).
visible_width = 90  # This is the width of the display area (terminal width).

# Define a repeating land (road) pattern.
land_base = "___*___-"
land_repeats = 200  # Increase or decrease this to change the total length of the road.
land_pattern = land_base * land_repeats

# Set initial positions.
cyclist_offset = 10      # Starting horizontal offset for the cyclist.
min_offset = 2          # Starting position for the cyclist.
max_offset = 50          # Maximum horizontal offset.
speed = 1                # Movement speed (how many spaces to move per frame).

land_offset = 0          # Initial scrolling offset for the road.

try:
    while True:
        # Clear the terminal screen ('cls' for Windows, 'clear' for Unix-based systems).
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Draw the cyclist at the current offset.
        for line in cyclist_art.splitlines():
            print(" " * cyclist_offset + line)
        
        # Print an empty line between the cyclist and the road.
        print()
        
        # Create a smoothly scrolling road by duplicating the land pattern.
        full_land = land_pattern + land_pattern  # Duplicate for seamless wrapping.
        display_land = full_land[land_offset:land_offset + visible_width]
        print(display_land)
        
        # Pause briefly (adjust speed as desired).
        time.sleep(0.1)
        
        # Update the road offset.
        land_offset = (land_offset + 1) % len(land_pattern)
        
        # Update the cyclist offset. When reaching the maximum, reset to start:
        cyclist_offset += speed
        if cyclist_offset > max_offset:
            cyclist_offset = min_offset

except KeyboardInterrupt:
    # Exit the loop gracefully on Ctrl-C.
    pass
