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
- high score, current score, lives

Extensions
- 2 players version

"""

# Constants
SIZE = 15
CANVAS_WIDTH = SIZE * 30
PLAY_HEIGHT = SIZE * 30
CANVAS_HEIGHT = PLAY_HEIGHT + 35

START_LENGTH = 3
START_DIRECTION = 'right'

BG_COLOR = 'white'
FILL_COLOR = 'black'
FADE_COLOR = '#BDBDBD'

MAX_TURNS = 5
SCORE_MULTIPLE = 10

# if you make this larger, the game will go slower
DELAY = 0.2
DELAY_INCREASE = 0.95

# Global
_is_cip = False

class Food:
    """
    Snake food
    """
    def __init__(self):
        self.food = None

    def _get_random_location(self):
        """
        Get a random x,y location on the canvas but not right against the walls
        """
        x = max(SIZE * random.randint(0, CANVAS_WIDTH//SIZE-1), SIZE)
        x = min(CANVAS_WIDTH-SIZE*2, x)
        y = max(SIZE * random.randint(0, PLAY_HEIGHT//SIZE-1), SIZE)
        y = min(PLAY_HEIGHT-SIZE*2, y)
        return x, y 

    def render(self, canvas):
        """
        Draw the food at random empty location
        """
        x, y = self._get_random_location()
        while canvas.find_overlapping(x, y, x+SIZE, y+SIZE):
            x, y = self._get_random_location()
        
        # Clear previous food
        if self.food:
            canvas.delete(self.food)

        self.food = canvas.create_oval(
            x,
            y,
            x+SIZE,
            y+SIZE,
            FILL_COLOR
        )

        # Update canvas
        update_canvas(canvas)


    def fade(self, canvas):
        """
        Fade out the food
        """
        canvas.set_color(self.food, FADE_COLOR)
        
        # Update canvas
        update_canvas(canvas)        

class Snake:
    """
    The snake
    """
    def __init__(self, length=1, direction='right'):
        self.direction = direction
        self.length = length
        self.snake = []

    def render(self, canvas):
        # Start in y location on the left half of the screen
        x = self.length*SIZE + SIZE
        y = SIZE * random.randint(0, PLAY_HEIGHT//SIZE-1)
        for i in range(self.length):
            self.snake.append(
                canvas.create_rectangle(
                    x - i*(SIZE) - SIZE,                    
                    y,
                    x - i*(SIZE),
                    y + SIZE,
                    FILL_COLOR
                )
            )

        # Update canvas
        update_canvas(canvas)

    def move(self, canvas, new_direction):
        """
        Move the snake by one step
        """
        head = self.snake[0]
        head_x = canvas.get_left_x(head)
        head_y = canvas.get_top_y(head)

        x_offset, y_offset = self._get_offset(new_direction)

        # If snake is one unit long, can just move one step
        if len(self.snake) == 1:
            canvas.move(self.snake[0], x_offset, y_offset)
            self.direction = new_direction
            return self.direction

        move_x = head_x + x_offset
        move_y = head_y + y_offset
        second_x = canvas.get_left_x(self.snake[1])
        second_y = canvas.get_top_y(self.snake[1])

        if move_x == second_x and move_y == second_y:
            # Moving into itself, ignore new direction
            # For example: Snake moving up and new direction is down
            x_offset, y_offset = self._get_offset(self.direction)
        else:
            # Update the current direction
            self.direction = new_direction

        # Check for walls
        new_x = head_x + x_offset
        new_y = head_y + y_offset        
        if self.direction == 'right' and new_x >= CANVAS_WIDTH:
            new_x = CANVAS_WIDTH - SIZE + 0.1
        elif self.direction == 'down' and new_y >= PLAY_HEIGHT:
            new_y = PLAY_HEIGHT - SIZE + 0.1    

        # Move the tail to the new head
        tail = self.snake.pop()
        canvas.moveto(tail, new_x, new_y)
        self.snake.insert(0, tail)
        
        # Update canvas
        update_canvas(canvas)        

        return self.direction

    def grow(self, canvas):
        # Grow the snake by one
        tail = self.snake[-1]
        tail_x = canvas.get_left_x(tail)
        tail_y = canvas.get_top_y(tail)

        # TODO: check if tail is touching wall
        if self.direction == 'left':
            tail_x += SIZE
        elif self.direction == 'right':
            tail_x -= SIZE
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

        # Update canvas
        update_canvas(canvas)        

    def fade(self, canvas):
        """
        Fade out the snake
        """
        for snake in self.snake:
            canvas.set_color(snake, FADE_COLOR)

        # Update canvas
        update_canvas(canvas)            
        
    def get_coords(self, canvas):
        """
        Return the x, y location of the head of the snake
        """
        return canvas.get_left_x(self.snake[0]), canvas.get_top_y(self.snake[0])

    def _get_offset(self, direction):
        """
        Get the x and y offset based on direction
        """
        move_x = 0
        move_y = 0
        if direction == 'left':
            move_x = -SIZE
            move_y = 0
        elif direction == 'right':
            move_x = SIZE
            move_y = 0
        elif direction == 'up':
            move_x = 0
            move_y = -SIZE
        elif direction == 'down':
            move_x = 0
            move_y = SIZE
        return move_x, move_y

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

def check_for_collisions(canvas, snake, food):
    """
    Milestone #4: Detecting collisions
    """
    is_game_over = False
    scored = False
    snake_x, snake_y = snake.get_coords(canvas)
    # Check for walls
    if snake_x < 0 or (snake_x+SIZE) > CANVAS_WIDTH:
        print("x out of bounds")
        is_game_over = True
        return is_game_over, scored

    if snake_y < 0 or (snake_y+SIZE) > PLAY_HEIGHT:
        print("y out of bounds")
        is_game_over = True
        return is_game_over, scored

    # Check for snake running into food or itself
    overlapping_list = canvas.find_overlapping(
        snake_x, snake_y, snake_x+SIZE, snake_y+SIZE)
    for overlapping in overlapping_list:
        if overlapping == snake.snake[0] or (snake.snake[1] and overlapping == snake.snake[1]):
            # Ignore the head section
            pass
        elif overlapping in snake.snake:
            # Ran into itself
            print("Snake ran into itself")
            is_game_over = True
            return is_game_over, scored
        elif overlapping == food.food:
            # Ran into food
            print("Snake ate food")
            food.render(canvas)
            snake.grow(canvas)
            scored = True

    return is_game_over, scored

def display_game_over(canvas):
    """
    Show game over message
    """
    font_size = 50
    font = 'sans-serif'
    text = "GAME OVER" 
    x = (CANVAS_WIDTH-len(text)*font_size/2)//2 - font_size
    y = (PLAY_HEIGHT-2*font_size)//2

    canvas.create_text(
        x,
        y,
        text, 
        font_size = font_size,
        font = font,
        color = FILL_COLOR
    )

    y += 2*font_size
    font_size = 20
    text = "Press [SPACE] to try again"
    
    canvas.create_text(
        x,
        y,
        text, 
        font_size = font_size,
        font = font,
        color = FILL_COLOR
    )

    # Update canvas
    update_canvas(canvas)    

    # Wait for keypress
    wait_for_key_press(canvas)    
    canvas.clear()    

def display_intro(canvas):
    """
    Show intro splash screen
    """
    font_size = 50
    font = 'sans-serif'
    text = "S N A K E"
    shadow_offset = 3
    #x = (CANVAS_WIDTH-210)//2
    x = (CANVAS_WIDTH-len(text)*font_size/2)//2
    y = (PLAY_HEIGHT-2*font_size)//2

    canvas.create_text(
        x+shadow_offset,
        y+shadow_offset,
        text, 
        font_size = font_size,
        font = font,
        color = FADE_COLOR
    )    
    
    canvas.create_text(
        x,
        y,
        text, 
        font_size = font_size,
        font = font,
        color = FILL_COLOR
    )

    y += 2*font_size
    font_size = 20
    text = "Press [SPACE] to start"
    
    canvas.create_text(
        x,
        y,
        text, 
        font_size = font_size,
        font = font,
        color = FILL_COLOR
    )    

    # Update canvas
    update_canvas(canvas)    

    # Wait for keypress
    wait_for_key_press(canvas)    
    canvas.clear()

def wait_for_key_press(canvas):
    """
    Sleep until any key is pressed
    """
    key = canvas.get_last_key_press()
    while not key or key[0] != ' ':
        key = canvas.get_last_key_press()
        time.sleep(DELAY) 

def display_scores(canvas, curr_high_score):
    """
    Render the score info
    """
    score = None
    high_score = None

    canvas.create_rectangle(
        0, PLAY_HEIGHT,
        CANVAS_WIDTH, CANVAS_HEIGHT,
        FILL_COLOR
    )

    font_size = 16
    font = 'sans-serif'
    text = "Score:"

    padding = 10
    x = padding
    y = PLAY_HEIGHT + padding
    canvas.create_text(
        x, y, 
        text = text,
        font_size = font_size,
        color = BG_COLOR
    )

    x = len(text)*font_size//2 + 2*padding
    text = "0"
    score = canvas.create_text(
        x, y, 
        text = text,
        font_size = font_size,
        color = BG_COLOR
    )

    text = "High Score:"
    x = CANVAS_WIDTH - len(text)*font_size
    canvas.create_text(
        x, y, 
        text = text,
        font_size = font_size,
        color = BG_COLOR
    )    

    x += len(text)*font_size//2 + 2*padding
    text = str(curr_high_score)
    high_score = canvas.create_text(
        x, y, 
        text = text,
        font_size = font_size,
        color = BG_COLOR
    )     

    # Update canvas
    update_canvas(canvas)

    return score, high_score

def update_scores(canvas, score, curr_score, high_score, curr_high_score):
    """
    Update the score stats on-screen
    """
    canvas.change_text(score, str(curr_score))
    canvas.change_text(high_score, str(curr_high_score))

    # Update canvas
    update_canvas(canvas)    

def play_snake(canvas, score, high_score, curr_high_score):
    """
    Play the game of snake
    """
    direction = START_DIRECTION
    delay = DELAY
    is_game_over = False
    current_score = 0
    snake = Snake(START_LENGTH, direction)
    snake.render(canvas)
    food = Food()
    food.render(canvas)

    # Animation loop
    while not is_game_over:

        # Move the player
        direction = get_direction(canvas, direction)
        direction = snake.move(canvas, direction)
        is_game_over, scored = check_for_collisions(canvas, snake, food)

        if scored:
            current_score += SCORE_MULTIPLE
            if current_score > curr_high_score:
                curr_high_score = current_score
            update_scores(canvas, score, current_score, high_score, curr_high_score)

            # Increase the speed
            delay *= DELAY_INCREASE
     
        # Update canvas
        update_canvas(canvas)

        # Sleep
        time.sleep(delay)

    # Grey out the game pieces
    snake.fade(canvas)
    food.fade(canvas)

    return curr_high_score

def update_canvas(canvas):
    """
    Call update canvas for non-CIP IDE
    """
    global _is_cip
    if not _is_cip:
        canvas.update()

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    if hasattr(canvas, 'canvas'):
        global _is_cip
        _is_cip = True
    
    high_score = 0
    
    # Splash screen
    display_intro(canvas)

    while True:
        # Game screen
        score_obj, high_score_obj = display_scores(canvas, high_score)

        # Play the game
        high_score = play_snake(canvas, score_obj, high_score_obj, high_score)

        # Display game over
        display_game_over(canvas)

    # wait for the user to close the window
    if not _is_cip:
        canvas.mainloop()            

if __name__ == '__main__':
    main()
