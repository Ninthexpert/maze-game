import tkinter as tk
import random

# Creates an empty maze

rows = 10
cols = 10
level = 1


# Sets the levels and difficulty
def get_level_settings():

    global rows
    global cols
    global wall_density

    if level == 1:

        rows = 10
        cols = 10
        wall_density = 0.30

    elif level == 2:

        rows = 15
        cols = 15
        wall_density = 0.40

    elif level == 3:

        rows = 20
        cols = 20
        wall_density = 0.50

get_level_settings()

def generate_maze():

    global maze
    global start_row
    global start_col
    global end_row
    global end_col
    # Variables for player and maze positions
    start_row = 0
    start_col = 0
    end_row = rows - 1
    end_col = cols - 1
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

            if (r, c) not in path:

                if random.random() < wall_density:

                    maze[r][c] = "#"

                else:

                    maze[r][c] = "."
    
    maze[0][0] = "S"
    maze[end_row][end_col] = "E"

generate_maze()
print(len(maze))
print(len(maze[0]))

def next_level():

    global level
    global player_row
    global player_col

    level += 1

    print("Current level:", level)

    if level > 3:

        print("YOU BEAT THE GAME")

        return
    
    get_level_settings()

    generate_maze()
    print("Exit:", end_row, end_col)
    print(maze[end_row][end_col])

    player_row = 0
    player_col = 0

    canvas.config(
        width=cols * CELL_SIZE,
        height=rows * CELL_SIZE
    )
    
    window.geometry(
    f"{cols * CELL_SIZE}x{rows * CELL_SIZE}"
    )

    global fog_enabled

    fog_enabled = False

    window.after(2000, enable_fog)
    draw_maze()

player_row = 0
player_col = 0

# Windows set up
window = tk.Tk()
window.title("Grid test")
CELL_SIZE = 25
window.geometry(
    f"{cols * CELL_SIZE}x{rows * CELL_SIZE}"
)


canvas = tk.Canvas(
    window,
    width = cols * CELL_SIZE,
    height = rows * CELL_SIZE
)

# Creates the maze, walls, and start and endzones
def draw_maze():
    canvas.delete("all")

    for row in range(rows):

        for col in range(cols):
            
            # Maze creation
            tile = maze[row][col]

            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE

            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            row_distance = abs(row - player_row)
            col_distance = abs(col - player_col)

            visible = (
                row_distance <= 1
                and
                col_distance <= 1
            )

            if fog_enabled and not visible:

                color = "grey"
            
            else:

                # Colors the squares
                if tile == "#":

                    color = "black"

                elif tile == "S":

                    color = "green"

                elif tile == "E":

                    color = "red"
                    print("Drawing exit at", row, col)

                else:

                    color = "white"
            # Creates the square with proper color
            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill = color,
                outline = "grey"
            )

    # Tracks player location
    x1 = player_col * CELL_SIZE + 5
    y1 = player_row * CELL_SIZE + 5

    x2 = x1 + CELL_SIZE - 10
    y2 = y1 + CELL_SIZE - 10

    # Creates player icon
    canvas.create_oval(
        x1,
        y1,
        x2,
        y2,
        fill="blue"
    )

# Player movement function    
def move_player(event):

    global player_row
    global player_col

    new_row = player_row
    new_col = player_col

    if event.keysym == "Up":

        new_row -= 1

    elif event.keysym == "Down":

        new_row += 1

    elif event.keysym == "Left":

        new_col -= 1

    elif event.keysym == "Right":

        new_col += 1

    if (
        0 <= new_row < rows
        and
        0 <= new_col < cols
    ):

        if maze[new_row][new_col] != "#":

            player_row = new_row
            player_col = new_col

            if (
                player_row == end_row
                and
                player_col == end_col
            ):

                next_level()

    draw_maze()

# Fog mechanics
fog_enabled = False

def enable_fog():
    global fog_enabled
    fog_enabled = True
    draw_maze()

canvas.pack()

draw_maze()

window.bind(
    "<Key>",
    move_player
)
window.after(2000, enable_fog)
window.mainloop()