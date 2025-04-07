import os
import time
import math
import sys
import colorama

colorama.init()

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

def move_cursor(y, x=0):
    """Move the cursor to a specific position"""
    sys.stdout.write(f"\033[{y};{x}H")
    sys.stdout.flush()

def clear_screen():
    """Clear the screen properly"""
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_bush(duration=3, colored=True):
    """
    Show animated bush for specified duration (in seconds)
    """
    # Parameters to control the swaying effect
    amplitude = 1.5    # Maximum horizontal offset
    frequency = 0.7    # How fast the wind oscillates
    frame_rate = 10    # Frames per second
    total_frames = int(duration * frame_rate)

    clear_screen()

    try:
        for frame in range(total_frames):
            # Calculate wave position based on frame
            t = frame / frame_rate
            
            # Move cursor to top of screen
            move_cursor(1, 0)
            
            # Draw the bush with wave effect
            for i, line in enumerate(bush):
                phase = i * math.pi / 6  # Different phase for each line
                offset = int(amplitude * math.sin(frequency * t + phase))
                
                # Print with consistent coloring
                if colored:
                    color_start = "\033[32m"  # Green
                    color_end = "\033[0m"     # Reset
                else:
                    color_start = ""
                    color_end = ""
                
                if offset >= 0:
                    print(" " * offset + color_start + line + color_end)
                else:
                    removal = abs(offset)
                    print(color_start + line[removal:] + color_end)
            
            # Short sleep for animation timing
            time.sleep(1/frame_rate)
            
    except KeyboardInterrupt:
        pass
    finally:
        # Clear screen when done
        clear_screen()

# For direct execution
if __name__ == "__main__":
    try:
        while True:
            animate_bush(duration=3)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass