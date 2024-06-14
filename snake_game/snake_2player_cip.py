from graphics import Canvas
import random
import time

"""
File: snake_2player.py

This script implements a 2-player game of snake
"""

SIZE = 15
CANVAS_WIDTH = SIZE * 30
PLAY_HEIGHT = SIZE * 30
CANVAS_HEIGHT = PLAY_HEIGHT + 35
    
BG_COLOR = 'black'
P1_COLOR = 'red'
P2_COLOR = 'blue'

P1_KEY_MAP = {
    'w':'U',
    'W':'U',    
    'a':'L',
    'A':'L',
    's':'D',
    'S':'D',
    'd':'R',
    'D':'R'
}

P2_KEY_MAP = {
    'ArrowLeft':'L',
    'Left':'L',    
    'ArrowRight':'R',
    'Right':'R',    
    'ArrowUp':'U',
    'Up':'U',    
    'ArrowDown':'D',
    'Down':'D'        
}

# if you make this larger, the game will go slower
DELAY = 0.2

class Snake:
    """
    The snake
    """
    def __init__(self, color, name='', direction='R', key_map={}):
        self.direction = direction
        self.name = name
        self.color = color
        self.key_map = key_map
        self.snake = []             # Store snake inverse; head is end of list

    def render(self, canvas):
        """
        Draw the snake
        """
        # Check starting direction
        if self.direction == 'R':
            #  Start on left side of screen
            x = max(SIZE, SIZE * random.randint(0, CANVAS_WIDTH//2//SIZE))
        else:
            # Start on right side of the screen 
            x = min(CANVAS_WIDTH-2*SIZE, CANVAS_WIDTH - SIZE * random.randint(0, CANVAS_WIDTH//2//SIZE))
        y = SIZE * random.randint(0, PLAY_HEIGHT//SIZE-1)
        self.snake.append(
            canvas.create_rectangle(
                x,
                y,
                x + SIZE,
                y + SIZE,
                self.color
            )
        )

    def _get_new_head(self, canvas, direction):
        """
        Get new head object based on direction
        """
        x, y = self.get_coords(canvas)
        if direction == 'L':
            x -= -SIZE
        elif direction == 'R':
            x += SIZE
        elif direction == 'U':
            y += -SIZE
        elif direction == 'D':
            y -= SIZE
        
        return canvas.create_rectangle(
            x, y, x+SIZE, y+SIZE, self.color)

    def move_and_grow(self, canvas, keys):
        """
        Move the head and grow snake by one
        """
        direction = self.direction

        # Process last key first
        for key in reversed(keys):
            if key in self.key_map.keys():
                print("[move]", self.name, direction, self.direction)
                direction = self.key_map[key]
                self.direction = direction
                break
        
        self.snake.append(self._get_new_head(canvas, direction))

    def check_for_collisions(self, canvas, ignore_list):
        """
        Return true if snake hit something
        """
        has_collision = False
        snake_x, snake_y = self.get_coords(canvas)

        print("[check]", self.name, self.direction, snake_x, snake_y)

        # Check for walls
        if snake_x <= 0 or (snake_x+SIZE) >= CANVAS_WIDTH:
            print(self.name, "x out of bounds")
            has_collision = True
            return has_collision

        if snake_y <= 0 or (snake_y+SIZE) >= PLAY_HEIGHT:
            print(self.name, "y out of bounds")
            has_collision = True
            return has_collision

        # Check for running into things
        overlapping_list = canvas.find_overlapping(
            snake_x, snake_y, snake_x+SIZE, snake_y+SIZE)
        for overlapping in overlapping_list:
            if overlapping in ignore_list:
                # Can ignore shapes in the ignore list
                pass
            elif overlapping == self.snake[-1]:
                # Can ignore head of snake
                pass
            else:
                has_collision = True
                return has_collision

        return has_collision

    def get_coords(self, canvas):
        """
        Return the x, y location of the head of the snake
        """
        return canvas.get_left_x(self.snake[-1]), canvas.get_top_y(self.snake[-1])

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    print("canvas:", CANVAS_WIDTH, CANVAS_HEIGHT, PLAY_HEIGHT)
    bg = canvas.create_rectangle(0, 0, CANVAS_WIDTH, PLAY_HEIGHT, BG_COLOR)
    ignore_list = [bg]

    is_game_over = False

    player_1 = Snake(P1_COLOR, 'Player 1', 'R', P1_KEY_MAP)
    player_1.render(canvas)
    print("player 1:", player_1.get_coords(canvas))
    player_2 = Snake(P2_COLOR, 'Player 2', 'L', P2_KEY_MAP)
    player_2.render(canvas)
    print("player 2:", player_2.get_coords(canvas))

    p1_game_over = False
    p2_game_over = False

    # Animation loop:
    while not is_game_over:
        
        # Get key presses
        keys = list(canvas.get_new_key_presses())
        player_1.move_and_grow(canvas, keys)
        player_2.move_and_grow(canvas, keys)
        #p1_game_over = player_1.check_for_collisions(canvas, ignore_list)
        #p2_game_over = player_2.check_for_collisions(canvas, ignore_list)
        

        if p1_game_over and p2_game_over:
            # Tie
            print("TIE!")
            is_game_over = True
        elif p1_game_over:
            # Player 1 lost
            print("Player 1 LOST")
            is_game_over = True
        elif p2_game_over:
            # Player 2 list
            print("Player 2 LOST")
            is_game_over = True

        # sleep
        time.sleep(DELAY)
 

if __name__ == '__main__':
    main()
