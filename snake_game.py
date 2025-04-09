import random
import uuid
import time
import curses

# Constants for the game
WIDTH = 80  # Width of the game board
HEIGHT = 20  # Height of the game board
SNAKE_CHAR = 'O'
FOOD_CHAR = '*'
EMPTY_CHAR = ' '

# Initialize the game state
snake = [(HEIGHT // 2, WIDTH // 2)]  # Start in the center of the board
direction = (0, 1)  # Start moving to the right
food = (random.randint(0, HEIGHT - 1), random.randint(0, WIDTH - 1))
food_guid = str(uuid.uuid4())  # Generate a GUID for the food

def generate_food():
    """Generate a new food position that is not on the snake."""
    while True:
        new_food = (random.randint(0, HEIGHT - 1), random.randint(0, WIDTH - 1))
        if new_food not in snake:
            return new_food

def draw_board(stdscr):
    """Draw the game board with visible walls."""
    stdscr.clear()
    # Draw the top and bottom walls
    for x in range(WIDTH + 2):
        stdscr.addch(0, x, '#')  # Top wall
        stdscr.addch(HEIGHT + 1, x, '#')  # Bottom wall

    # Draw the left and right walls
    for y in range(1, HEIGHT + 1):
        stdscr.addch(y, 0, '#')  # Left wall
        stdscr.addch(y, WIDTH + 1, '#')  # Right wall

    # Draw the snake and food inside the walls
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (y, x) in snake:
                stdscr.addch(y + 1, x + 1, SNAKE_CHAR)  # Offset by 1 for walls
            elif (y, x) == food:
                stdscr.addch(y + 1, x + 1, FOOD_CHAR)  # Offset by 1 for walls
            else:
                stdscr.addch(y + 1, x + 1, EMPTY_CHAR)  # Offset by 1 for walls

    # Display the food GUID and instructions
    stdscr.addstr(HEIGHT + 2, 0, f"Food GUID: {food_guid}")
    stdscr.addstr(HEIGHT + 3, 0, "Use arrow keys to move. Press Q to quit.")
    stdscr.refresh()

def move_snake():
    """Move the snake in the current direction."""
    global food, food_guid
    head = snake[-1]
    new_head = (head[0] + direction[0], head[1] + direction[1])

    # Check for collisions with walls or itself
    if (new_head[0] < 0 or new_head[0] >= HEIGHT or
        new_head[1] < 0 or new_head[1] >= WIDTH or
        new_head in snake):
        raise Exception("Game Over!")  # End the game if collision occurs

    # Check if the snake eats the food
    if new_head == food:
        snake.append(new_head)  # Grow the snake
        food = generate_food()  # Generate new food
        food_guid = str(uuid.uuid4())  # Generate a new GUID for the food
    else:
        snake.append(new_head)  # Move the snake
        snake.pop(0)  # Remove the tail

def change_direction(new_direction):
    """Change the direction of the snake."""
    global direction
    # Prevent the snake from reversing
    if (direction[0] + new_direction[0] != 0 or
        direction[1] + new_direction[1] != 0):
        direction = new_direction

def main(stdscr):
    global direction
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(200)

    while True:
        # Reset the game state for a new game
        global snake, direction, food, food_guid
        snake = [(HEIGHT // 2, WIDTH // 2)]  # Reset snake to the center
        direction = (0, 1)  # Reset direction to move right
        food = generate_food()  # Generate new food
        food_guid = str(uuid.uuid4())  # Generate a new GUID for the food

        while True:
            try:
                draw_board(stdscr)
                move_snake()

                # Handle user input
                key = stdscr.getch()
                if key == curses.KEY_UP:
                    change_direction((-1, 0))
                elif key == curses.KEY_DOWN:
                    change_direction((1, 0))
                elif key == curses.KEY_LEFT:
                    change_direction((0, -1))
                elif key == curses.KEY_RIGHT:
                    change_direction((0, 1))
                elif key == ord('q'):
                    stdscr.addstr(HEIGHT + 3, 0, "Game Quit!")
                    stdscr.refresh()
                    time.sleep(1)
                    return  # Exit the game
            except Exception as e:
                # Display "Snake Crash! Try Again?" and restart option without clearing the screen
                stdscr.addstr(HEIGHT // 2, WIDTH // 2 - 10, "Snake Crash! Try Again?", curses.A_BOLD)
                stdscr.addstr(HEIGHT // 2 + 1, WIDTH // 2 - 15, "Press R to restart or Q to quit.", curses.A_BOLD)
                stdscr.refresh()

                # Wait for user input to restart or quit
                while True:
                    key = stdscr.getch()
                    if key == ord('r'):  # Restart the game
                        break
                    elif key == ord('q'):  # Quit the game
                        return

if __name__ == "__main__":
    curses.wrapper(main)
