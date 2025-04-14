#!/usr/bin/env python3
import random
import os
import time
import sys
import re

# --- Helper functions for terminal display ---

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def reveal(text, delay=0.01):
    """Prints text with a typing effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Function to remove ANSI color codes, so box widths aren't miscalculated.
ANSI_PATTERN = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
def strip_ansi_codes(s):
    return ANSI_PATTERN.sub('', s)

def colored_text(text, color_code):
    # ANSI escape codes: green=32, yellow=33, red=31
    return f"\033[{color_code}m{text}\033[0m"

def hp_bar(current, maximum, bar_length=20):
    ratio = current / maximum
    filled_length = int(ratio * bar_length)
    empty_length = bar_length - filled_length
    # Color: green > 50%, yellow between 25% and 50%, red if below 25%
    if ratio > 0.5:
        color = 32  # green
    elif ratio > 0.25:
        color = 33  # yellow
    else:
        color = 31  # red
    bar = colored_text("█" * filled_length, color)
    bar += "░" * empty_length
    return bar

def print_box(title, lines):
    """
    Prints a box with a title and content lines (list of strings).
    Properly accounts for ANSI color codes so alignment doesn't break.
    """
    # First, strip ANSI codes when measuring content width:
    stripped_title = strip_ansi_codes(title)
    stripped_lines = [strip_ansi_codes(line) for line in lines]
    # Build content lines with a leading/trailing space
    content = [f" {line} " for line in lines]
    
    width = max(len(stripped_title) + 4, max(len(s) for s in [f" {ln} " for ln in stripped_lines]))  
    top = "┌" + "─" * width + "┐"
    mid_title = f"│ {title.center(width - 2)} │"
    sep = "├" + "─" * width + "┤"
    
    print(top)
    print(mid_title)
    print(sep)
    for line in content:
        # Right-pad the line to match the box width. 
        # (Strip ANSI codes for length, but keep them in the actual printed string)
        stripped_len = len(strip_ansi_codes(line))
        padding = width - stripped_len
        print("│" + line + " " * padding + "│")
    print("└" + "─" * width + "┘")

# --- Global constants and initial stats ---
MAX_TURNS = 20
PLAYER_MAX_HP = 50
PLAYER_SPEED = 50     # for turn order
BOSS_SPEED = 40       # boss speed
ULTRABALL_MULTIPLIER = 2.0

# Boss stats for Shadow Gyarados (no HP, but catch-related stats)
BOSS_CATCH_RATE = 15.0
BOSS_EVASION = 15.0   # not directly used, but available

# Damage values
NORMAL_ATTACK_DAMAGE = 1
ULTIMATE_DAMAGE = 15

# --- Player inventory and stats tracking ---
player_hp = PLAYER_MAX_HP
ultraballs = 5
razz_used = 0
golden_razz_used = 0
rocks_used = 0

# Bonus accumulators for catch chance (in %)
berry_bonus = 0.0

# Boss “Leap of Evolution” (charge) value
leap = 0

# Flag if boss is caught
boss_caught = False

# --- Utility: Check if we should trigger ultimate immediately ---
def check_for_ultimate():
    """
    If the boss's Leap of Evolution is >= 4, 
    trigger the boss_ultimate() immediately (and repeat if still >=4).
    This does not use up a turn.
    """
    global leap, boss_caught
    while leap >= 4 and not boss_caught:
        boss_ultimate()

# --- Catch attempt function ---
def attempt_catch():
    global ultraballs, berry_bonus, leap, boss_caught
    if ultraballs <= 0:
        reveal("You have no Ultraballs left!")
        return
    ultraballs -= 1
    effective_catch = min(BOSS_CATCH_RATE * ULTRABALL_MULTIPLIER + berry_bonus, 100.0)
    roll = random.uniform(0, 100)
    reveal(f"\nAttempting catch with effective chance {effective_catch:.2f}% (rolled {roll:.2f})")
    if roll <= effective_catch:
        reveal("\n⭐⭐ Congratulations! You have caught Shadow Gyarados! ⭐⭐")
        boss_caught = True
    else:
        reveal("\nThe catch failed... Shadow Gyarados smirks and its charge increases!")
        leap = min(leap + 1, 100)
        check_for_ultimate()  # Check if ultimate triggers immediately after raising leap

# --- Boss ultimate move: Dragon Breath ---
def boss_ultimate():
    global leap, player_hp
    reveal("\n*** Shadow Gyarados unleashes its ULTIMATE move: Dragon Breath! ***")
    # Deduct 4 leaps
    leap -= 4
    print("\nChoose your dodge option:")
    print("1. Stand your ground")
    print("2. Dodge left")
    print("3. Dodge right")
    
    bad_choice = str(random.choice([1, 2, 3]))
    choice = input("Enter your choice (1, 2, or 3): ").strip()
    if choice == bad_choice:
        reveal("\nOh no! You failed to dodge the Dragon Breath!")
        player_hp = max(player_hp - ULTIMATE_DAMAGE, 0)
        reveal(f"You take {ULTIMATE_DAMAGE} damage!")
    else:
        reveal("\nYou dodged the Dragon Breath successfully!")

# --- Boss move (if no ultimate triggered) ---
def boss_move():
    global leap, player_hp
    move_roll = random.uniform(0, 100)
    if move_roll <= 70:
        # Dragon Tail
        reveal("\nShadow Gyarados uses Dragon Tail!")
        leap = min(leap + 1, 100)
        player_hp = max(player_hp - NORMAL_ATTACK_DAMAGE, 0)
        reveal(f"Dragon Tail increases boss charge by 1 and deals {NORMAL_ATTACK_DAMAGE} damage.")
        check_for_ultimate()  # immediate ultimate if needed
    else:
        # Dragon Pulse
        gained = random.randint(1, 3)
        reveal("\nShadow Gyarados uses Dragon Pulse and charges up!")
        leap = min(leap + gained, 100)
        reveal(f"It gains {gained} charge(s) (Leap of Evolution now {leap}).")
        check_for_ultimate()  # immediate ultimate if needed

# --- Player move processing ---
def player_move():
    global berry_bonus, leap, razz_used, golden_razz_used, rocks_used
    moves = [
        "Throw a Razz Berry (+0.5% catch chance)",
        "Throw a Golden Razz Berry (+2% catch chance, but boss gains 1 leap)",
        "Throw a Rock (50% chance to reset boss's charge; on failure boss gains 4 leaps)",
        "Throw an Ultraball (attempt to catch Shadow Gyarados)"
    ]
    print_box("Your Moves", [f"{i+1}. {moves[i]}" for i in range(len(moves))])
    move = input("Enter the number of your move (1-4): ").strip()
    if move == "1":
        reveal("\nYou toss a Razz Berry at Shadow Gyarados!")
        berry_bonus += 0.5
        razz_used += 1
        reveal("Catch chance increased by 0.5% for your next catch attempt.")
    elif move == "2":
        reveal("\nYou toss a Golden Razz Berry at Shadow Gyarados!")
        berry_bonus += 2.0
        golden_razz_used += 1
        leap = min(leap + 1, 100)
        reveal("Catch chance increased by 2%, but Shadow Gyarados gains 1 leap charge!")
        check_for_ultimate()
    elif move == "3":
        reveal("\nYou throw a Rock at Shadow Gyarados!")
        rocks_used += 1
        if random.choice([True, False]):
            leap = 0
            reveal("The Rock shattered Shadow Gyarados’s concentration! Its charge resets to 0!")
        else:
            leap = min(leap + 4, 100)
            reveal("The Rock missed! Shadow Gyarados roars and instantly gains 4 leaps!")
            check_for_ultimate()
    elif move == "4":
        reveal("\nYou hurl an Ultraball at Shadow Gyarados!")
        attempt_catch()
    else:
        reveal("Invalid move. You lose your turn!")

# --- Display current status ---
def display_status(turns_left):
    clear_screen()
    boss_lines = [
        f"Turns left: {turns_left}",
        f"Leap of Evolution: {leap}"
    ]
    print_box("Boss Data: Shadow Gyarados", boss_lines)
    
    player_lines = [
        f"HP: {player_hp}/{PLAYER_MAX_HP} {hp_bar(player_hp, PLAYER_MAX_HP)}",
        f"Ultraballs: {ultraballs}",
        f"Razz Berries used: {razz_used}",
        f"Golden Razz Berries used: {golden_razz_used}",
        f"Rocks thrown: {rocks_used}",
        f"Catch bonus: {berry_bonus:.2f}%"
    ]
    print_box("Player Status", player_lines)
    print()  # Extra spacing

# --- Welcome instructions ---
def welcome_screen():
    clear_screen()
    tips = [
        "Welcome to the Shadow Gyarados Boss Fight Test!",
        "",
        "Tips and Boss Mechanics:",
        " • Shadow Gyarados has no HP; you must catch it.",
        " • Each turn consists of your move and then the boss move.",
        " • Moves:",
        "   - Razz Berry: +0.5% catch chance.",
        "   - Golden Razz Berry: +2% catch chance, but boss gains 1 charge.",
        "   - Rock: 50% chance to reset boss charge; else boss gains 4 charges.",
        "   - Ultraball: Attempt to catch (uses a ball).",
        " • Boss moves:",
        "   - Dragon Tail (70% chance): Deals 1 damage and adds 1 charge.",
        "   - Dragon Pulse (30% chance): Adds 1-3 charges.",
        "   - Ultimate (Dragon Breath): Triggers immediately at 4+ charges.",
        "",
        "Defeat the boss by catching it before 20 turns, or avoid taking too much damage!"
    ]
    print_box("WELCOME & TIPS", tips)
    input("\nPress Enter to begin the battle...")

# --- Main battle loop ---
def battle():
    global player_hp, leap, boss_caught
    current_turn = 1
    
    while current_turn <= MAX_TURNS and not boss_caught and player_hp > 0:
        display_status(MAX_TURNS - current_turn + 1)
        print(f"--- Turn {current_turn} ---")
        
        # Player’s turn first if speeds are equal or player is faster
        if PLAYER_SPEED >= BOSS_SPEED:
            player_move()
            if boss_caught or player_hp <= 0:
                break
            if not boss_caught and player_hp > 0:
                # Boss move
                boss_move()
        else:
            # Boss goes first if boss is faster
            boss_move()
            if boss_caught or player_hp <= 0:
                break
            if not boss_caught and player_hp > 0:
                player_move()
        
        # Pause briefly so the player can read the outcome
        time.sleep(2)
        current_turn += 1

    display_status(0)
    if boss_caught:
        reveal("\nBattle Over: You captured Shadow Gyarados!")
    elif player_hp <= 0:
        reveal("\nBattle Over: Defeated!!! Level up more and try again.......")
    else:
        reveal("\nBattle Over: ROAR!!!!! Shadow Gyarados flees into the darkness...")

# --- Main entry point ---
if __name__ == "__main__":
    welcome_screen()
    battle()
    reveal("\nThank you for playing!")
