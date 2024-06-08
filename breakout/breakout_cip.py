from graphics import Canvas
import time
import random
import math

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 600
PADDLE_Y = CANVAS_HEIGHT - 30
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 15
BALL_RADIUS = 10
BALL_SIZE = BALL_RADIUS*2

BRICK_FROM_TOP = 50
BRICK_GAP = 5
BRICK_WIDTH = (CANVAS_WIDTH - BRICK_GAP*9) / 10
BRICK_HEIGHT = 10

NUM_COL = 10
NUM_ROW = 10

COLORS = ["red", "orange", "yellow", "green", "cyan"]

DELAY = 0.1 
VELOCITY = 20

MAX_TURNS = 5
BRICK_SCORE = 100

def setup_world(canvas):
    """
    Add the top bricks, ball and paddle to the canvas
    """
    # Create the bricks
    x = 0
    y = BRICK_FROM_TOP
    for col in range(NUM_COL):
        for row in range(NUM_ROW):
            canvas.create_rectangle(
                BRICK_GAP*row + x + row*BRICK_WIDTH,
                BRICK_GAP*col + y + col*BRICK_HEIGHT,
                BRICK_GAP*row + x + row*BRICK_WIDTH + BRICK_WIDTH,
                BRICK_GAP*col + y + col*BRICK_HEIGHT + BRICK_HEIGHT,
                COLORS[col//2]
            )

    # Create the ball
    x = CANVAS_WIDTH/2
    y = CANVAS_HEIGHT/2
    ball = canvas.create_oval(
        x, 
        y,
        x + BALL_SIZE,
        y + BALL_SIZE,
        'blue'     
    )

    # Create the paddle
    paddle = canvas.create_rectangle(
        0,
        PADDLE_Y,
        PADDLE_WIDTH,
        PADDLE_Y + PADDLE_HEIGHT,
        'black'
    )

    # Create the score text
    padding = 10
    font_size = 16
    label = "Points:"
    canvas.create_text(
        padding,
        padding,
        text = label,
        font_size = font_size,
        color = 'black'
    )

    points = canvas.create_text(
        len(label)*font_size,
        padding,
        text = "0",
        font_size = font_size,
        color = 'black'
    )    

    # Create the lives text
    label = "Lives:"
    canvas.create_text(
        CANVAS_WIDTH - len(label)*font_size,
        padding,
        text = label,
        font_size = font_size,
        color = 'black'
    ) 

    lives = canvas.create_text(
        CANVAS_WIDTH - padding - font_size,
        padding,
        text = str(MAX_TURNS),
        font_size = font_size,
        color = 'black'
    )     

    return paddle, ball, points, lives

def move_ball(canvas, ball, change_x, change_y):
    """
    One move of the ball
    """
    left_x, top_y, right_x, bottom_y = get_corner_coordinates(canvas, ball)
    
    # At left wall
    if left_x <= 0:
        change_x = -change_x
    
    # At right wall
    if right_x >= CANVAS_WIDTH:
        change_x = -change_x

    # At top wall
    if top_y <= 0:
        change_y = -change_y

    # Move the ball
    canvas.move(ball, change_x, change_y)

    # Return the modified change_x and change_y values
    return change_x, change_y

def move_paddle(canvas, paddle):
    """
    Move the paddle based on the location of the mouse
    """
    mouse_x = canvas.get_mouse_x()
    mouse_x = min(mouse_x, CANVAS_WIDTH-PADDLE_WIDTH)
    canvas.moveto(paddle, mouse_x, PADDLE_Y)

def game_over(canvas, is_win):
    """
    Show appropriate game over message
    """
    x = 100
    font_size = 50
    text = "GAME OVER"
    if is_win:
        text = "YOU WIN!"
        x = 130
    
    canvas.create_text(
        x,
        CANVAS_HEIGHT/2 + BRICK_FROM_TOP,
        text = text,
        font_size = font_size,
        color = 'black'
    )

def get_corner_coordinates(canvas, canvas_obj):
    """
    Takes a canvas object and returns the coordinates as a tuple in the form of
    (left_x, top_y, right_x, bottom_y).
    """
    left_x, top_y = canvas.coords(canvas_obj)
    right_x = left_x + canvas.get_object_width(canvas_obj)
    bottom_y = top_y + canvas.get_object_height(canvas_obj)
    
    return left_x, top_y, right_x, bottom_y


def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    # Setup the world
    paddle, ball, points_text, lives_text = setup_world(canvas)

    # Animation loop
    turns = 0
    score = 0
    change_x = VELOCITY
    change_y = VELOCITY    
    while turns < MAX_TURNS and score < BRICK_SCORE*NUM_ROW*NUM_COL:
        
        # Paddle follow the mouse
        move_paddle(canvas, paddle)

        # Move the ball
        change_x, change_y = move_ball(canvas, ball, change_x, change_y)

        # Check for bottom wall
        ball_y = canvas.get_top_y(ball) + BALL_SIZE
        if ball_y >= CANVAS_HEIGHT:
            # Reset the ball
            turns += 1
            canvas.change_text(lives_text, str(MAX_TURNS-turns))
            print("Out of bounds! {} lives left".format(MAX_TURNS-turns))
            change_x = VELOCITY
            change_y = VELOCITY
            canvas.moveto(ball, CANVAS_WIDTH/2 + BALL_RADIUS, CANVAS_HEIGHT/2 + BALL_RADIUS)

        # Check for collisions
        collisions = canvas.find_overlapping(*get_corner_coordinates(canvas, ball))
        for collision in collisions:
            if collision == ball:
                # Ignore the ball
                pass
            elif collision == paddle:
                # Hit the paddle
                change_y = -change_y
            else:
                # Hit a brick
                score += BRICK_SCORE
                canvas.change_text(points_text, str(score))
                change_y = -change_y
                canvas.delete(collision)

        # Sleep
        time.sleep(DELAY)                 

    # Show game over text
    game_over(canvas, score == BRICK_SCORE*NUM_ROW*NUM_COL)

if __name__ == '__main__':
    main()
