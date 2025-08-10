import curses
from curses import wrapper
import time
import random

# -------------------------------
# Function to display the start screen
# -------------------------------
def start_screen(stdscr):
    # Clear any previous content
    stdscr.clear()
    # Print welcome message
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    # Wait for user input before starting
    stdscr.getkey()


# -------------------------------
# Function to display the typing text and WPM
# -------------------------------
def display_text(stdscr, target, current, wpm=0):
    # Display the target text at the top
    stdscr.addstr(target)
    # Display the current WPM below it
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    # Loop through each typed character
    for i, char in enumerate(current):
        correct_char = target[i]
        # Default to green if correct
        color = curses.color_pair(1)
        # Red if incorrect
        if char != correct_char:
            color = curses.color_pair(2)

        # Display the typed character with its respective color
        stdscr.addstr(0, i, char, color)


# -------------------------------
# Function to load random text from a file
# -------------------------------
def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        # Choose a random line, strip newline
        return random.choice(lines).strip()


# -------------------------------
# Main typing test logic
# -------------------------------
def wpm_test(stdscr):
    target_text = load_text()        # The text to type
    current_text = []                # What the user has typed so far
    wpm = 0                          # Words per minute
    start_time = time.time()         # Start timer
    stdscr.nodelay(True)             # Non-blocking input (typing without waiting for Enter)

    while True:
        # Calculate elapsed time (avoid division by zero)
        time_elapsed = max(time.time() - start_time, 1)
        # WPM formula: (characters typed / 5) / (minutes elapsed)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        # Clear screen and redraw text + WPM
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        # If user typed the full target text
        if "".join(current_text) == target_text:
            # Stop accepting fast inputs (return to blocking mode)
            stdscr.nodelay(False)
            stdscr.clear()
            # Show final text and WPM result
            display_text(stdscr, target_text, current_text, wpm)
            stdscr.addstr(2, 0, f"You completed the text! Final WPM: {wpm}")
            stdscr.addstr(4, 0, "Press any key to continue...")
            stdscr.refresh()
            # Wait for user to press a key before exiting
            stdscr.getkey()
            break

        # Try to get user input without blocking
        try:
            key = stdscr.getkey()
        except:
            # If no key pressed yet, continue loop
            continue

        # If ESC key is pressed, quit the test
        if ord(key) == 27:
            break

        # Handle backspace
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        # Handle normal key typing (only if not past target length)
        elif len(current_text) < len(target_text):
            current_text.append(key)


# -------------------------------
# Main program function
# -------------------------------
def main(stdscr):
    # Color pair definitions:
    # 1 = Green text (correct letters)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    # 2 = Red text (incorrect letters)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    # 3 = White text (default)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Show welcome screen
    start_screen(stdscr)
    while True:
        # Run the WPM test
        wpm_test(stdscr)
        # After test completion, ask user to retry or exit
        stdscr.addstr(6, 0, "Press ESC to exit or any key to try again...")
        key = stdscr.getkey()
        if ord(key) == 27:
            break


# -------------------------------
# Entry point for curses program
# -------------------------------
wrapper(main)

