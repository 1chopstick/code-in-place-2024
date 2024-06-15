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

FILL_COLOR = 'white'
BG_COLOR = 'black'
P1_COLOR = '#D0312D'        # Red
P1_FADE_COLOR = '#FFCCCB'
P2_COLOR = '#3944BC'        # Blue
P2_FADE_COLOR = '#ADD8E6'
FADE_COLOR = 'grey'

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
    def __init__(self, color, fade_color, name='', direction='R', key_map={}):
        self.direction = direction
        self.name = name
        self.color = color
        self.fade_color = fade_color
        self.key_map = key_map
        self.snake = []             # Store snake inverse; head is end of list

    def render(self, canvas):
        """
        Draw the snake
        """
        # Check starting direction
        if self.direction == 'R':
            #  Start on left side of screen heading right
            x = max(SIZE, SIZE * random.randint(0, CANVAS_WIDTH//2//SIZE))
        else:
            # Start on right side of the screen heading left
            x = min(CANVAS_WIDTH-2*SIZE, CANVAS_WIDTH - SIZE * random.randint(0, CANVAS_WIDTH//2//SIZE))
        y = min(PLAY_HEIGHT-SIZE, SIZE * random.randint(0, PLAY_HEIGHT//SIZE))
        self.snake.append(
            canvas.create_rectangle(
                x,
                y,
                x + SIZE,
                y + SIZE,
                self.color
            )
        )

    def fade(self, canvas):
        """
        Fade out the color
        """
        for shape in self.snake:
            canvas.set_color(shape, self.fade_color)

    def _get_new_location(self, canvas, direction):
        """
        Get new head object based on direction
        """
        x, y = self.get_coords(canvas)
        if direction == 'L':
            x += -SIZE
        elif direction == 'R':
            x += SIZE
        elif direction == 'U':
            y += -SIZE
        elif direction == 'D':
            y += SIZE
        return min(x, x+SIZE), min(y, y+SIZE)

    def move_and_grow(self, canvas, keys):
        """
        Move the head and grow snake by one
        """
        direction = self.direction
        new_x = None
        new_y = None

        # Process last key first
        for key in reversed(keys):
            if key in self.key_map.keys():
                direction = self.key_map[key]

                # Is direction valid?
                new_x, new_y = self._get_new_location(canvas, direction)
                if len(self.snake) > 1:
                    second_x = canvas.get_left_x(self.snake[-2])
                    second_y = canvas.get_top_y(self.snake[-2])
                    if new_x == second_x and new_y == second_y:
                        # Moving into itself, ignore new direction
                        # For example: Snake moving up and new direction is down
                        new_x, new_y = self._get_new_location(canvas, self.direction)
                    else:
                        # Update the current direction
                        self.direction = direction   
                else:
                    # Update the current direction
                    self.direction = direction                       
                break

        # Move snake by one unit
        if not new_x:
            new_x, new_y = self._get_new_location(canvas, self.direction)

        self.snake.append(
            canvas.create_rectangle(new_x, new_y, new_x+SIZE, new_y+SIZE, self.color)
        )

    def check_for_collisions(self, canvas, ignore_list):
        """
        Return true if snake hit something
        """
        has_collision = False
        snake_x, snake_y = self.get_coords(canvas)
        
        # Check for walls
        if snake_x < 0 or (snake_x+SIZE) > CANVAS_WIDTH:
            print(self.name, "x out of bounds")
            has_collision = True
            return has_collision

        if snake_y < 0 or (snake_y+SIZE) > PLAY_HEIGHT:
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

def _add_intro_text(canvas, x, y, text, font_size, color=FILL_COLOR):
    """
    Add text to introduction splash page
    """
    font = 'sans-serif'    
    return canvas.create_text(
        x,
        y,
        text, 
        font_size = font_size,
        font = font,
        color = color
    )   

def _add_intro_arrows(canvas, x, y, size, direction, color=FILL_COLOR):
    """
    Draw arrow direction icons
    """
    coords_dict = {
        'U':[x + size/2, y, x, y+size, x+size, y+size],
        'D':[x, y, x + size, y, x+size/2, y+size],
        'L':[x+size, y+size, x+size, y, x, y+size/2],
        'R':[x, y, x+size, y+size/2, x, y+size]
    }
    coords = coords_dict[direction]
    canvas.create_polygon(
        *coords,
        color=FILL_COLOR
    )

def display_intro(canvas):
    """
    Show intro splash screen
    """
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, BG_COLOR)

    font_size = 20
    x = 25
    y = PLAY_HEIGHT//4
    text = "TWO PLAYERS"
    _add_intro_text(canvas, x, y, text, font_size)

    y += font_size + 5
    font_size = 50
    shadow_offset = 3
    text = "S N A K E"
    _add_intro_text(canvas, x-shadow_offset, y-shadow_offset, text, font_size, P1_COLOR)
    _add_intro_text(canvas, x+shadow_offset, y+shadow_offset, text, font_size, P2_COLOR)
    _add_intro_text(canvas, x, y, text, font_size)

    # Player 1 Info
    y += 2*font_size
    p2_y = y
    font_size = 20
    padding = 10
    text = "Player 1"
    _add_intro_text(canvas, x, y, text, font_size, P1_COLOR)

    # UP
    x = 25
    y += font_size + padding
    _add_intro_arrows(canvas, x, y, font_size, 'U')
    x += 4*padding
    text = "[W] key"
    _add_intro_text(canvas, x, y, text, font_size)

    # DOWN
    x = 25
    y += font_size + padding
    _add_intro_arrows(canvas, x, y, font_size, 'D')
    x += 4*padding
    text = "[S] key"
    _add_intro_text(canvas, x, y, text, font_size)

    # LEFT
    x = 25
    y += font_size + padding
    _add_intro_arrows(canvas, x, y, font_size, 'L')
    x += 4*padding
    text = "[A] key"
    _add_intro_text(canvas, x, y, text, font_size)

    # RIGHT
    x = 25
    y += font_size + padding
    _add_intro_arrows(canvas, x, y, font_size, 'R')
    x += 4*padding
    text = "[D] key"
    _add_intro_text(canvas, x, y, text, font_size)

    # Space to continue
    y += 5*padding
    x = 25
    font_size = 20
    text = "Press [SPACE] to start"
    _add_intro_text(canvas, x, y, text, font_size)

    # Player 2 Info
    text = "Player 2"
    y = p2_y
    x = 250
    _add_intro_text(canvas, x, y, text, font_size, P2_COLOR)

    # UP
    x = 250
    y += font_size + padding
    _add_intro_arrows(canvas, x, y, font_size, 'U')
    x += 4*padding
    text = "[UP] key"
    _add_intro_text(canvas, x, y, text, font_size)

    # DOWN
    x = 250
    y += font_size + padding
    _add_intro_arrows(canvas, x, y, font_size, 'D')
    x += 4*padding
    text = "[DOWN] key"
    _add_intro_text(canvas, x, y, text, font_size)

    # LEFT
    x = 250
    y += font_size + padding
    _add_intro_arrows(canvas, x, y, font_size, 'L')    
    x += 4*padding
    text = "[LEFT] key"
    _add_intro_text(canvas, x, y, text, font_size)

    # RIGHT
    x = 250
    y += font_size + padding
    _add_intro_arrows(canvas, x, y, font_size, 'R')  
    x += 4*padding
    text = "[RIGHT] key"
    _add_intro_text(canvas, x, y, text, font_size)

    # Wait for keypress
    wait_for_key_press(canvas)    
    canvas.clear()

def display_footer(canvas, p1_score, p2_score):
    """
    Render the score info
    """
    p1_score_obj = None
    p2_score_obj = None

    font_size = 16
    font = 'sans-serif'
    padding = 10

    text = "Player 1:"
    x = padding
    y = PLAY_HEIGHT + padding
    canvas.create_text(
        x, y, 
        text = text,
        font_size = font_size,
        color = P1_COLOR
    )

    x = len(text)*font_size//2 + 2*padding
    text = str(p1_score)
    p1_score_obj = canvas.create_text(
        x, y, 
        text = text,
        font_size = font_size,
        color = BG_COLOR
    )

    text = "Player 2:"
    x = CANVAS_WIDTH - len(text)*font_size
    canvas.create_text(
        x, y, 
        text = text,
        font_size = font_size,
        color = P2_COLOR
    )    

    x += len(text)*font_size//2 + 2*padding
    text = str(p2_score)
    p2_score_obj = canvas.create_text(
        x, y, 
        text = text,
        font_size = font_size,
        color = BG_COLOR
    )        
    return p1_score_obj, p2_score_obj

def wait_for_key_press(canvas):
    """
    Sleep until any key is pressed
    """
    key = canvas.get_last_key_press()
    while not key or key[0] != ' ':
        key = canvas.get_last_key_press()
        time.sleep(DELAY) 

def display_game_over(canvas, winner):
    """
    Show game over message
    """
    font_size = 50
    font = 'sans-serif'

    if not winner:
        text = "DRAW!"
    else:
        text = "PLAYER " + str(winner) + " WINS!"
    x = 25
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
    text = "Press [SPACE] to play again"
    
    canvas.create_text(
        x,
        y,
        text, 
        font_size = font_size,
        font = font,
        color = FILL_COLOR
    )        

    # Wait for keypress
    wait_for_key_press(canvas)    
    canvas.clear()    


def play_snake(canvas, ignore_list):
    """
    Play the game of snake
    """
    is_game_over = False
    winner = None

    # Create player 1
    player_1 = Snake(P1_COLOR, P1_FADE_COLOR, 'Player 1', 'R', P1_KEY_MAP)
    player_1.render(canvas)

    # Create player 2
    player_2 = Snake(P2_COLOR, P2_FADE_COLOR, 'Player 2', 'L', P2_KEY_MAP)
    player_2.render(canvas)

    # Animation loop:
    while not is_game_over:
        
        # Get key presses
        keys = list(canvas.get_new_key_presses())
        player_1.move_and_grow(canvas, keys)
        player_2.move_and_grow(canvas, keys)
        p1_game_over = player_1.check_for_collisions(canvas, ignore_list)
        p2_game_over = player_2.check_for_collisions(canvas, ignore_list)
        
        if p1_game_over and p2_game_over:
            # Tie
            winner = None
            is_game_over = True
        elif p1_game_over:
            # Player 1 lost
            winner = 2
            is_game_over = True
        elif p2_game_over:
            # Player 2 list
            winner = 1
            is_game_over = True

        # sleep
        time.sleep(DELAY)

    player_1.fade(canvas)
    player_2.fade(canvas)
    return winner

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    # Splash screen
    display_intro(canvas)


    # Play game
    is_game_over = False
    player1_score = 0
    player2_score = 0

    while True:

        # Setup the game
        bg = canvas.create_rectangle(0, 0, CANVAS_WIDTH, PLAY_HEIGHT, BG_COLOR)
        ignore_list = [bg]    
        p1_score_obj, p2_score_obj = display_footer(canvas, player1_score, player2_score)

        # Play the game
        winner = play_snake(canvas, ignore_list)
        if winner == 1:
            player1_score += 1
        elif winner == 2:
            player2_score += 1
        canvas.change_text(p1_score_obj, str(player1_score))
        canvas.change_text(p2_score_obj, str(player2_score))

        # Display game over
        display_game_over(canvas, winner)        
        

if __name__ == '__main__':
    main()
