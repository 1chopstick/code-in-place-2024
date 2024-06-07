from graphics import Canvas
import time
import random
    
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
SIZE = 20

# if you make this larger, the game will go slower
DELAY = 0.1 


def get_direction(canvas, direction):
    """
    Milestone #3: Handle Key Press
    """ 
    key = canvas.get_last_key_press()

    if not key:
        return direction

    if 'Left' in key:
        direction = 'left'
        print('left arrow pressed!')
    if 'Right' in key:
        direction = 'right'
        print('right arrow pressed!')
    if 'Up' in key:
        direction = 'up'
        print('up arrow pressed!')
    if 'Down' in key:
        direction = 'down'
        print('down arrow pressed!')
    return direction

def setup_world(canvas):
    """
    Milestone #1: Set up the World
    """

    # Create the player
    x = 0
    y = 0
    player = canvas.create_rectangle(
        x,
        y,
        x+SIZE,
        y+SIZE,
        'blue'
    )

    # Create the goal
    x = CANVAS_WIDTH - 2*SIZE
    y = CANVAS_HEIGHT - 2*SIZE
    goal = canvas.create_rectangle(
        x,
        y,
        x+SIZE,
        y+SIZE,
        'salmon'
    )

    # Create the score text
    offset = 10
    canvas.create_text(
        offset,
        CANVAS_HEIGHT - SIZE - offset,
        text = "Points:",
        font_size = SIZE,
        color = 'black'
    )

    points = canvas.create_text(
        80,
        CANVAS_HEIGHT - SIZE - offset,
        text = "0",
        font_size = SIZE,
        color = 'black'
    )

    return player, goal, points

def game_over(canvas):
    canvas.create_text(
        75,
        CANVAS_HEIGHT/2,
        text = "GAME OVER",
        font_size = SIZE*2,
        color = 'black'
    )
    pass


def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    # Setup the world
    player, goal, score = setup_world(canvas)

    direction = 'right'     # left, right, up or down
    move_x = SIZE
    move_y = 0
    points = 0

    # Wait for mouse click to start
    canvas.wait_for_click()

    # Milestone #2: Animate
    while True:

        # Move the player
        direction = get_direction(canvas, direction)
        if direction == 'left':
            move_x = -SIZE
            move_y = 0
        if direction == 'right':
            move_x = SIZE
            move_y = 0
        if direction == 'up':
            move_x = 0
            move_y = -SIZE
        if direction == 'down':
            move_x = 0
            move_y = SIZE
        canvas.move(player, move_x, move_y)

        # sleep
        time.sleep(DELAY)        

        # Milestone #4: Detecting collisions
        player_x = canvas.get_left_x(player)
        player_y = canvas.get_top_y(player)
        goal_x = canvas.get_left_x(goal)
        goal_y = canvas.get_top_y(goal)
        
        # Check if player hits the wall
        if player_x < 0 or (player_x+SIZE) > CANVAS_WIDTH:
            print("x out of bounds")
            break

        if player_y < 0 or (player_y+SIZE) > CANVAS_HEIGHT:
            print("y out of bounds")
            break

        # Milestone #5: Moving the goal
        if player_x == goal_x and player_y == goal_y:
            print("Hit the goal!")
            points += 1
            canvas.change_text(score, str(points))

            # Move the goal in multiples of SIZE
            goal_x = SIZE * random.randint(0, CANVAS_WIDTH//SIZE-1)
            goal_y = SIZE * random.randint(0, CANVAS_HEIGHT//SIZE-1)
            canvas.moveto(goal, goal_x, goal_y)

    game_over(canvas)
    print("GAME OVER!")


if __name__ == '__main__':
    main()
