from graphics import Canvas
import random
import time

"""
File: snake.py

This script implements the full game of snake

Reference: https://playsnake.org/

Tips:

Represent your snake using a list of rectangles (where the rectangles are the 
shapes returned by create_rect). This will make it much easier to move your snake. 
You will only need to change the head and the tail.

Use the find_overlapping function to tell if you have hit yourself.

Design:
- start with one squares
- each time you eat a food, you get longer by one square
- food is circle
- track points
- track time
- food cannot appear where snake is located

"""
    
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
SIZE = 15

BG_COLOR = 'white'
FILL_COLOR = 'black'


# if you make this larger, the game will go slower
DELAY = 0.1

class Food:
    """
    Snake food
    """
    def __init__(self):
        self.food = None

    def _get_random_location(self):
        return SIZE * random.randint(0, CANVAS_WIDTH//SIZE-1), SIZE * random.randint(0, CANVAS_HEIGHT//SIZE-1)

    def render(self, canvas):
        """
        Draw the food at random empty location
        """
        x, y = self._get_random_location()
        while canvas.find_overlapping(x, y, x+SIZE, y+SIZE):
            x, y = self._get_random_location()
        
        self.food = canvas.create_oval(
            x,
            y,
            x+SIZE,
            y+SIZE,
            FILL_COLOR
        )
        print("food:", x, y)

class Snake:
    """
    The snake
    """
    def __init__(self, length=1, direction='right'):
        self.direction = direction
        self.length = length
        self.snake = []

    def render(self, canvas):
        # Start in random location on the left half of the screen
        x = random.randint(0, CANVAS_WIDTH/2)
        y = random.randint(0, CANVAS_HEIGHT-SIZE)
        print(x, y)
        for i in range(self.length):
            self.snake.append(
                canvas.create_rectangle(
                    x + i*(SIZE),
                    y,
                    x + i*(SIZE) + SIZE,
                    y + SIZE,
                    FILL_COLOR
                )
            )

    def move(self, canvas, x_offset, y_offset, direction):
        """
        Move the snake to the provided x, y offset
        """
        collision = False
        head = self.snake[0]
        head_x = canvas.get_left_x(head)
        head_y = canvas.get_top_y(head)

        # If snake one unit long, just move it
        if len(self.snake) == 1:
            canvas.move(self.snake[0], x_offset, y_offset)
            return collision

        # TODO: what if tail move out of the way in time?

        # Move the head
        overlapping_list = canvas.find_overlapping(
            x_offset, y_offset, x_offset+SIZE, y_offset+SIZE)
        if self.snake[1] not in overlapping_list:
            # Move the tail to the new head
            tail = self.snake.pop()
            self.snake.insert(0, tail)
            canvas.moveto(
                tail,
                head_x + x_offset,
                head_y + y_offset
            )
            # Update the current direction
            self.direction = direction

        else:
            # Direction does not change
            pass

        return collision

    def grow(self, canvas):
        # Grow the snake by one
        tail = self.snake[-1]
        tail_x = canvas.get_left_x(tail)
        tail_y = canvas.get_top_y(tail)

        # TODO: check if tail is touching wall
        if self.direction == 'left':
            tail_x += SIZE
        elif self.direction == 'right':
            tail_x -+ SIZE
        elif self.direction == 'up':
            tail_y += SIZE
        elif self.direction == 'down':
            tail_y -= SIZE

        self.snake.append(
            canvas.create_rectangle(
                tail_x,
                tail_y,
                tail_x + SIZE,
                tail_y + SIZE,
                FILL_COLOR
            )
        )


def get_direction(canvas, direction):
    """
    Milestone #3: Handle Key Press
    """ 
    key = canvas.get_last_key_press()

    if not key:
        return direction

    if 'Left' in key:
        direction = 'left'
    if 'Right' in key:
        direction = 'right'
    if 'Up' in key:
        direction = 'up'
    if 'Down' in key:
        direction = 'down'
    return direction

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    snake = Snake(15, 'right')
    snake.render(canvas)

    food = Food()
    food.render(canvas)

    direction = 'right'     # left, right, up or down
    move_x = SIZE
    move_y = 0

    # Animation loop
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
        collision = snake.move(canvas, move_x, move_y, direction)
        snake.grow(canvas)

        # sleep
        time.sleep(DELAY)                


if __name__ == '__main__':
    main()
