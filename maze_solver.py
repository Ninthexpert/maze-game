import random
import msvcrt
import os

# Gets input from the user on how big the maze should be
rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))

# Creates an empty maze
maze = []

for r in range(rows):
    row = []

    for c in range(cols):
        row.append("*")

    maze.append(row)

# Uses path to find a guaranteed path through the maze
path = []

current_row = 0
current_col = 0

path.append((current_row,current_col))

# Continues to find path until the end (bottom right corner)
while current_row < rows - 1 or current_col < cols - 1:

    # If I am at the bottom of the maze, I can only go right
    if (current_row == rows - 1):
        current_col += 1
    
    # If I am at the right-most part of the maze, I can only go down
    elif (current_col== cols - 1):
        current_row += 1

    # If I have no restrictions, go down or right randomly
    else: 

        move = random.choice(["down","right"])

        if (move == "down"):
            current_row += 1
        
        else: 
            current_col += 1

    path.append((current_row,current_col))

# Add random walls for the maze
for r in range(rows):

    for c in range(cols):

        if (r,c) not in path:

            if(random.random() < 0.4): 
                maze[r][c] = "#"

# Add start, end, and display the maze
start_row = 0
start_col = 0
end_row = rows - 1
end_col = cols - 1
maze[0][0] = "S"
maze[end_row][end_col] = "E"

# Player position
player_row = start_row
player_col = start_col

# Print the maze
def print_maze():

    os.system("cls")

    print("\nUse Arrow Keys To Move")
    print("Reach E to win!\n")

    # Top border
    print("╔" + "══" * cols + "╗")

    for r in range(rows):

        print("║", end="")

        for c in range(cols):

            if r == player_row and c == player_col:
                print("P ", end="")

            elif r == end_row and c == end_col:
                print("E ", end="")

            elif maze[r][c] == "#":
                print("██", end="")

            else:
                print("  ", end="")

        print("║")

    # Bottom border
    print("╚" + "══" * cols + "╝")

# ==========================================
# GAME LOOP
# ==========================================

while True:

    print_maze()

    key = msvcrt.getch()

    # Arrow keys start with b'\xe0'
    if key == b'\xe0':

        key = msvcrt.getch()

        new_row = player_row
        new_col = player_col

        # UP
        if key == b'H':
            new_row -= 1

        # DOWN
        elif key == b'P':
            new_row += 1

        # LEFT
        elif key == b'K':
            new_col -= 1

        # RIGHT
        elif key == b'M':
            new_col += 1

        # Check boundaries
        if (
            0 <= new_row < rows
            and
            0 <= new_col < cols
        ):

            # Check wall collision
            if maze[new_row][new_col] != "#":

                player_row = new_row
                player_col = new_col

                # Check victory
                if (
                    player_row == end_row
                    and
                    player_col == end_col
                ):

                    print_maze()

                    print("YOU ESCAPED THE MAZE")
                    break