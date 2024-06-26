from graphics import Canvas
import random
import math
import time

"""
File: mastermind-mobile.py

This script implements the classical game of Mastermind.
Your task is to guess the color of the four circles on the decoding board.
This is the mobile-friendly version, without drag-and-drop animation

"""

# Constants
NUM_CIRCLES = 4
MAX_GUESSES = 12

CODE_SIZE = 35
CODE_PADDING = 20
KEY_SIZE = 16
KEY_PADDING = 4
KEY_EXACT_COLOR = 'red'
KEY_PARTIAL_COLOR = 'grey'
BUTTON_WIDTH = 70
BUTTON_HEIGHT = CODE_SIZE

COLORS = ['red', 'orange', '#FEF250', 'green', 'blue', 'purple']
MEDIUM_COLORS = ['salmon']
HARD_COLORS = ['salmon', 'brown', 'black']
EMPTY_FILL_COLOR = 'white'
OUTLINE_COLOR = 'black'
LIGHT_GRAY = '#e9e9e9'
GRAY = '#d4d4d4'
DARK_GRAY = '#9a9a9a'

CANVAS_WIDTH = 510
CANVAS_HEIGHT = max(MAX_GUESSES+2, len(COLORS)+len(HARD_COLORS)+2) * (CODE_SIZE+CODE_PADDING) + CODE_PADDING
DELAY = 0.1

# Global
_is_cip = False

class GameSettings:
    """
    Configuration object containing graphics and functions to allow the user to change 
    game settings
    """
    def __init__(self):
        self.difficulty = 1                 # selected difficulty level
        self.has_duplicates = False         # selected duplicate setting
        self.easy_button = []               # list of graphic objects in easy setting
        self.medium_button = []             # list of graphic objects in medium setting
        self.hard_button = []               # list of graphic objects in hard setting
        self.expert_button = []             # list of graphic objects in expert setting
        self.difficulty_arrow = None        # selection arrow for difficulty setting
        self.duplicate_arrow = None         # selection arrow for duplicate setting
        self.yes_button = []                # list of graphic objects in yes setting
        self.no_button = []                 # list of graphic objects in no setting
        self.start_button = []              # list of graphic objects in start button
        
        # maps [x,y] locations of selection arrow to selection
        self.arrow_location = {1:[], 2:[], 3:[], 4:[], "yes":[], "no":[]}

    def render(self, canvas):
        """
        Render the graphical components of the configuration screen
        """
        # Choose difficulty
        x = CODE_PADDING
        y = 100
        text = 'Choose difficulty:'
        self._render_config_headers(canvas, x, y, text)

        # Easy        
        x = CODE_PADDING + CODE_SIZE
        y += CODE_SIZE + CODE_PADDING
        self.easy_button.append(self._render_bg_button(canvas, x, y))

        color = 'green'
        self.easy_button.append(
            canvas.create_oval(
                x,
                y,
                x+CODE_SIZE,
                y+CODE_SIZE,
                color,
                OUTLINE_COLOR
            )
        )
        text = "EASY"
        x = CODE_PADDING + 2*CODE_SIZE + CODE_PADDING
        self.easy_button.append(self._render_config_text(canvas, x, y, text))

        # Selector arrow
        x = CODE_PADDING
        self.difficulty_arrow = self._render_arrow(canvas, x, y)
        self.arrow_location[1] = [x, y]

        # Medium
        color = 'blue'
        x = CODE_PADDING + CODE_SIZE
        y += CODE_SIZE + CODE_PADDING
        self.medium_button.append(self._render_bg_button(canvas, x, y))
        self.medium_button.append(
            canvas.create_rectangle(
                x,
                y,
                x+CODE_SIZE,
                y+CODE_SIZE,
                color,
                OUTLINE_COLOR
            )
        )    
        x = CODE_PADDING + 2*CODE_SIZE + CODE_PADDING
        text = "MEDIUM"
        self.medium_button.append(self._render_config_text(canvas, x, y, text))    

        # Selector arrow
        x = CODE_PADDING
        self.arrow_location[2] = [x, y]                

        # Hard
        color = 'black'
        x = CODE_PADDING + CODE_SIZE
        y += CODE_SIZE + CODE_PADDING
        self.hard_button.append(self._render_bg_button(canvas, x, y))
        self.hard_button.append(
            canvas.create_polygon(
                x + CODE_SIZE/2, y,
                x + CODE_SIZE, y + CODE_SIZE/2,
                x + CODE_SIZE/2, y + CODE_SIZE,
                x, y + CODE_SIZE/2,
                color=color,
                outline=OUTLINE_COLOR
            )
        )
        x = CODE_PADDING + 2*CODE_SIZE + CODE_PADDING
        text = "HARD"
        self.hard_button.append(self._render_config_text(canvas, x, y, text))

        # Selector arrow
        x = CODE_PADDING
        self.arrow_location[3] = [x, y]          

        # Expert  
        color = 'black'
        x = CODE_PADDING + CODE_SIZE
        y += CODE_SIZE + CODE_PADDING
        self.expert_button.append(self._render_bg_button(canvas, x, y))
        self.expert_button.append(
            canvas.create_polygon(
                x + CODE_SIZE/4, y,
                x + CODE_SIZE/2, y + CODE_SIZE/2,
                x + CODE_SIZE/4, y + CODE_SIZE,
                x, y + CODE_SIZE/2,
                color=color,
                outline=OUTLINE_COLOR
            )
        )
        self.expert_button.append(
            canvas.create_polygon(
                x + CODE_SIZE/4 + CODE_SIZE/2, y,
                x + CODE_SIZE, y + CODE_SIZE/2,
                x + CODE_SIZE/4 + CODE_SIZE/2, y + CODE_SIZE,
                x + CODE_SIZE/2, y + CODE_SIZE/2,
                color=color,
                outline=OUTLINE_COLOR
            )
        )        
        x = CODE_PADDING + 2*CODE_SIZE + CODE_PADDING
        text = "EXPERT"
        self.expert_button.append(self._render_config_text(canvas, x, y, text))

        # Selector arrow
        x = CODE_PADDING
        self.arrow_location[4] = [x, y]        

        # Choose duplicates
        x = CODE_PADDING
        y += 2*(CODE_SIZE + CODE_PADDING)        
        text = 'Allow duplicates?'
        self._render_config_headers(canvas, x, y, text)

        # Yes
        x = CODE_PADDING + CODE_SIZE
        y += CODE_SIZE + CODE_PADDING
        self.yes_button.append(self._render_bg_button(canvas, x, y))
        colors = ['red', 'red', 'red', 'red']
        self.yes_button += self._render_circles(canvas, x, y+2*KEY_PADDING, colors)        
        x += NUM_CIRCLES*(KEY_SIZE+KEY_PADDING) + CODE_PADDING
        text = "YES"
        self.yes_button.append(self._render_config_text(canvas, x, y, text))

        # Selector arrow
        x = CODE_PADDING
        self.arrow_location["yes"] = [x, y]        
        
        # No
        x = CODE_PADDING + CODE_SIZE
        y += CODE_SIZE + CODE_PADDING
        self.no_button.append(self._render_bg_button(canvas, x, y))
        colors = ['red', 'orange', 'green', 'blue']
        self.no_button += self._render_circles(canvas, x, y+2*KEY_PADDING, colors)        
        x += NUM_CIRCLES*(KEY_SIZE+KEY_PADDING) + CODE_PADDING
        text = "NO"
        self.no_button.append(self._render_config_text(canvas, x, y, text))        

        # Selector arrow
        x = CODE_PADDING
        self.duplicate_arrow = self._render_arrow(canvas, x, y)  
        self.arrow_location["no"] = [x, y]             

        # Play button
        x = CODE_PADDING
        y += 2*(CODE_SIZE + CODE_PADDING)
        offset = 5
        start_width = 150
        start_height = CODE_PADDING + CODE_PADDING
        self.start_button.append(
            canvas.create_polygon(
                x-offset, y-offset,
                x + start_width + offset, y-offset,
                x + start_width, y,
                x, y+start_height, 
                x-offset, y + start_height + offset,
                color=LIGHT_GRAY,
                outline=LIGHT_GRAY
            )
        )
        self.start_button.append(
            canvas.create_polygon(
                x + start_width + offset, y-offset,
                x + start_width, y,
                x, y + start_height,
                x-offset, y + start_height + offset,
                x + start_width + offset, y + start_height + offset,
                color=DARK_GRAY,
                outline=DARK_GRAY
            )
        )
        self.start_button.append(
            canvas.create_rectangle(
                x,
                y,
                x + start_width,
                y + start_height,
                GRAY,
                GRAY
            )
        )
        padding = 5
        text = 'START'
        self.start_button.append(
            self._render_config_headers(canvas, x+CODE_PADDING, y+padding, text)
        )

        # Update
        update_canvas(canvas)       

    def _render_bg_button(self, canvas, x, y):
        """
        Render rectangle background for selections
        """
        global _is_cip
        color = EMPTY_FILL_COLOR
        if not _is_cip:
            color = ''

        width = 200            
        return canvas.create_rectangle(
            x - KEY_PADDING,
            y - KEY_PADDING,
            x + KEY_PADDING + width,
            y + KEY_PADDING + CODE_SIZE,
            color,
            color
        )
        # Update
        update_canvas(canvas)  

    def _render_circles(self, canvas, x, y, colors):
        """
        Render the circle icons for duplicate settings
        """
        circles = []
        for i in range(NUM_CIRCLES):
            circles.append(
                canvas.create_oval(
                    x + i*KEY_SIZE + KEY_PADDING + i*KEY_PADDING,
                    y,
                    x + i*KEY_SIZE + KEY_PADDING + KEY_SIZE + + i*KEY_PADDING,
                    y+KEY_SIZE,
                    colors[i],
                    OUTLINE_COLOR
                )
            )

        # Update
        update_canvas(canvas)

        return circles

    def _render_arrow(self, canvas, x, y):
        """
        Render the selection arrow
        """
        offset = 8
        color = '#FEF250'
        return canvas.create_polygon(
            x+offset, y+offset,
            x+offset, y+CODE_SIZE-offset,
            x+CODE_SIZE-offset, y+CODE_SIZE/2,
            color=color,
            outline=OUTLINE_COLOR
        )

        # Update
        update_canvas(canvas)   

    def _move_arrow(self, canvas, arrow, selection):
        """
        Move the arrow graphic to the selected setting
        """
        offset = 8
        if selection in self.arrow_location and self.arrow_location[selection]:
            x = self.arrow_location[selection][0] + offset
            y = self.arrow_location[selection][1] + offset
            canvas.moveto(arrow, x, y)
        
        # Update
        update_canvas(canvas)  

    def _render_config_headers(self, canvas, x, y, text):
        """
        Render heading text
        """
        font_size = CODE_SIZE
        font = 'sans-serif'
        return canvas.create_text(
            x, 
            y, 
            text, 
            font_size = font_size,
            font = font,
            color = OUTLINE_COLOR
        )

        # Update
        update_canvas(canvas)

    def _render_config_text(self, canvas, x, y, text):
        """
        Render configuration label text
        """
        font = 'sans-serif'
        font_size = 26
        text_padding = (CODE_SIZE - font_size)/2
        return canvas.create_text(
                x, 
                y+text_padding, 
                text, 
                font_size = font_size,
                font = font,
                color = OUTLINE_COLOR
            )   

        # Update
        update_canvas(canvas)

    def handle_config(self, canvas):
        """
        Handles the user interactions with the configuration settings
        """
        done = False
        while not done:
            canvas.wait_for_click()
            click = canvas.get_last_click()
            if click:
                mouse_x, mouse_y = click
                selected_list = canvas.find_overlapping(
                    mouse_x, mouse_y, mouse_x, mouse_y
                )
                for selected in selected_list:
                    if selected in self.easy_button:
                        self.difficulty = 1
                        self._move_arrow(canvas, self.difficulty_arrow, 1)

                    elif selected in self.medium_button:
                        self.difficulty = 2
                        self._move_arrow(canvas, self.difficulty_arrow, 2)

                    elif selected in self.hard_button:
                        self.difficulty = 3
                        self._move_arrow(canvas, self.difficulty_arrow, 3)

                    elif selected in self.expert_button:
                        self.difficulty = 4
                        self._move_arrow(canvas, self.difficulty_arrow, 4)                        

                    elif selected in self.yes_button:
                        self.has_duplicates = True
                        self._move_arrow(canvas, self.duplicate_arrow, "yes")

                    elif selected in self.no_button:
                        self.has_duplicates = False
                        self._move_arrow(canvas, self.duplicate_arrow, "no")

                    elif selected in self.start_button:
                        done = True


class ColorPicker:
    """
    Color palette class to allow the user to select and assign colors to code pegs
    """
    def __init__(self, canvas, x, y, colors):
        self.left_x = x
        self.top_y = y
        self.colors = colors
        self.palette = {}
        self.selected_palette = None
        self.selected_color = None

    def render(self, canvas):
        """
        Draw the color swatches
        """
        for i in range(len(self.colors)):
            self.palette[canvas.create_oval(
                self.left_x,
                self.top_y + i*(CODE_SIZE+CODE_PADDING),
                self.left_x + CODE_SIZE,
                self.top_y + i*(CODE_SIZE+CODE_PADDING) + CODE_SIZE,
                self.colors[i]
            )] = self.colors[i]
        
        # Update
        update_canvas(canvas)
    
    def set_color(self, canvas, palette, selected_color):
        """
        Assign the selected color
        """
        self.selected_color = selected_color
        palette_x = canvas.get_left_x(palette)
        palette_y = canvas.get_top_y(palette)
        padding = 10
        self.selected_palette = canvas.create_oval(
            palette_x - padding/2,
            palette_y - padding/2,
            palette_x + CODE_SIZE + padding/2,
            palette_y + CODE_SIZE + padding/2,
            selected_color,
            OUTLINE_COLOR
        )

        # Update
        update_canvas(canvas)

    def reset(self, canvas):
        """
        Clear the selected color
        """
        self.selected_color = None
        if self.selected_palette:
            canvas.delete(self.selected_palette)

        # Update
        update_canvas(canvas)      


class Guess:
    """
    Class representing one guess of the game. Contains the graphic and functions 
    for the code pegs, key pegs, and check button
    """
    def __init__(self, canvas, x, y, num_pegs):
        self.left_x = x
        self.top_y = y
        self.guesses = ['' for _ in range(num_pegs)]
        self.codes = []
        self.num_pegs = num_pegs
        self.button = []

    def render(self, canvas):
        """
        Draw the code pegs and key pegs
        """
        # Draw the code pegs
        for i in range(self.num_pegs):
            self.codes.append(canvas.create_oval(
                self.left_x + i*(CODE_SIZE+CODE_PADDING),
                self.top_y,
                self.left_x + i*(CODE_SIZE+CODE_PADDING) + CODE_SIZE,
                self.top_y +CODE_SIZE,
                EMPTY_FILL_COLOR,
                OUTLINE_COLOR
            ))

        # Update
        update_canvas(canvas)

    def _render_keys(self, canvas, colors):
        """
        Render the feedback key pegs
        """
        # Draw the key pegs
        x = self.left_x + (CODE_SIZE+CODE_PADDING)*self.num_pegs
        color_index = 0
        for i in range(2):
            for j in range(self.num_pegs//2):
                canvas.create_oval(
                    x + j*(KEY_SIZE+KEY_PADDING),
                    self.top_y + i*(KEY_SIZE+KEY_PADDING),
                    x + j*(KEY_SIZE+KEY_PADDING) + KEY_SIZE,
                    self.top_y + i*(KEY_SIZE+KEY_PADDING) + KEY_SIZE,
                    colors[color_index],
                    OUTLINE_COLOR
                )
                color_index += 1

        # Update
        update_canvas(canvas)      

    def _render_button(self, canvas, is_on = False):
        """
        Render the check button
        """
        for item in self.button:
            canvas.delete(item)
        self.button = []

        x = self.left_x + (CODE_SIZE+CODE_PADDING)*self.num_pegs
        y = self.top_y
        offset = 4
    
        # Draw the button background (top)
        self.button.append(
            canvas.create_polygon(
                x-offset, y-offset,
                x + BUTTON_WIDTH + offset, y-offset,
                x + BUTTON_WIDTH, y,
                x, y+BUTTON_HEIGHT, 
                x-offset, y + BUTTON_HEIGHT + offset,
                color=LIGHT_GRAY,
                outline=LIGHT_GRAY
            )
        )

        # Draw the button background (bottom)
        self.button.append(
            canvas.create_polygon(
                x + BUTTON_WIDTH + offset, y-offset,
                x + BUTTON_WIDTH, y,
                x, y + BUTTON_HEIGHT,
                x-offset, y + BUTTON_HEIGHT + offset,
                x + BUTTON_WIDTH + offset, y + BUTTON_HEIGHT + offset,
                color=DARK_GRAY,
                outline=DARK_GRAY
            )
        )        

        # Draw the Check button
        self.button.append(
            canvas.create_rectangle(
                x,
                self.top_y,
                x + BUTTON_WIDTH,
                self.top_y + BUTTON_HEIGHT,
                GRAY,
                GRAY
            )
        )

        # Draw the label
        color = DARK_GRAY
        if is_on:
            color = OUTLINE_COLOR
        label = "Check"
        font_size = 16
        font = 'sans-serif'
        padding = 10
        self.button.append(
            canvas.create_text(
                x + padding,
                self.top_y + padding,
                label,
                font_size = font_size,
                font = font,
                color = color
            )
        )

        # Update
        update_canvas(canvas)

    def show_button(self, canvas):
        """
        Show the 'Check' button
        """
        self._render_button(canvas)

    def set_guess(self, canvas, code, color):
        """
        Change color of Code peg
        """
        for i in range(len(self.codes)):
            if code == self.codes[i]:
                self.guesses[i] = color

        # Update the color
        canvas.set_color(code, color)

        # Enable the check button if done
        if not self.has_blanks():
            self._render_button(canvas, True)

        # Update
        update_canvas(canvas)

    def has_blanks(self):
        """
        Returns true if there are blanks in the code guesses
        """
        has_blanks = False
        for guess in self.guesses:
            if guess == '':
                return True

        return has_blanks

    def check(self, canvas, truth):
        """
        Update the key pegs and return True if the Code pegs matches the truth list
        - red key means color and position is correct
        - grey key means color is correct but position is incorrect
        """
        # Compare color of key pegs to truth
        key_matches = []
        key_index = 0
        unmatched_indices = []
        unmatched_truth = []

        # Check for exact matches
        for i in range(self.num_pegs):
            if self.guesses[i] == truth[i]:
                key_matches.append(KEY_EXACT_COLOR)
            else:
                unmatched_indices.append(i)
                unmatched_truth.append(truth[i])

        # Check for partial matches
        for i in unmatched_indices:
            if self.guesses[i] in unmatched_truth:
                key_matches.append(KEY_PARTIAL_COLOR)
                unmatched_truth.remove(self.guesses[i])

        # Delete the Check button
        for item in self.button:
            canvas.delete(item)
        self.button = []

        # Render the key pegs
        peg_colors = [ EMPTY_FILL_COLOR for _ in range(self.num_pegs)]
        for i in range(len(key_matches)):
            peg_colors[i] = key_matches[i]
        self._render_keys(canvas, peg_colors)
    
        # Update
        update_canvas(canvas)

        return self.guesses == truth


def game_over(canvas, truth, is_winner, num_pegs):
    """
    Show appropriate game over message
    """
    padding = 5
    x = 100
    y = 2 * (CODE_PADDING + CODE_SIZE + CODE_PADDING)
    font_size = 50
    text = "GAME OVER"
    if is_winner:
        text = "YOU WIN!"
        x = 130
    
    canvas.create_rectangle(
        CODE_SIZE, 
        y, 
        CANVAS_WIDTH-CODE_SIZE, 
        y+font_size+CODE_SIZE+CODE_PADDING, 
        EMPTY_FILL_COLOR, 
        OUTLINE_COLOR
    )
    canvas.create_text(
        x,
        y+padding,
        text = text,
        font_size = font_size,
        color = 'black'
    )   

    # Show solution
    truth_x = (CANVAS_WIDTH - (num_pegs*(CODE_SIZE+CODE_PADDING)))/2        
    truth_y = y + font_size + padding
    for i in range(num_pegs):
        canvas.create_oval(
            truth_x + i*(CODE_SIZE + CODE_PADDING),
            truth_y,
            truth_x + i*(CODE_SIZE + CODE_PADDING) + CODE_SIZE,
            truth_y + CODE_SIZE,
            truth[i],
            'black'
        )

    # Update
    update_canvas(canvas)  

def get_overlapping(canvas):
    """
    Return list of shapes located at last mouse click
    Returns [] if no clicks
    """
    canvas.wait_for_click()
    click = canvas.get_last_click()
    if click:
        mouse_x, mouse_y = click
        overlapping_list = canvas.find_overlapping(
            mouse_x, mouse_y, mouse_x, mouse_y)
        return overlapping_list
    return []
                             

def play_row(canvas, guess, color_picker, truth):
    """
    Handle playing a row of guesses. 
    Actions are:
    - Picking a new color
    - Assiging a color to a Code peg
    - Click on the Check button
    """
    is_correct = False
    is_done = False
    selected_color = None 
    while not is_done:
        overlapping_list = get_overlapping(canvas)
        if overlapping_list:
            for overlapping in overlapping_list:
                if overlapping in guess.button:
                    # Clicked on Check button
                    if guess.has_blanks():
                        pass
                    else:
                        is_correct = guess.check(canvas, truth)
                        is_done = True

                    selected_color = None
                    color_picker.reset(canvas)

                elif selected_color is None and overlapping in color_picker.palette.keys():
                    # Clicked on color picker
                    selected_color = color_picker.palette[overlapping]                    
                    color_picker.set_color(canvas, overlapping, selected_color)

                elif selected_color and overlapping in color_picker.palette.keys():
                    # Switch to different color picker
                    color_picker.reset(canvas)
                    selected_color = color_picker.palette[overlapping]                    
                    color_picker.set_color(canvas, overlapping, selected_color)

                elif selected_color and overlapping in guess.codes:
                    # Clicked on code peg
                    guess.set_guess(canvas, overlapping, selected_color)
                    selected_color = None
                    color_picker.reset(canvas)

    return is_correct

def display_header(canvas):
    """
    Render the heading
    """
    font_size = CODE_SIZE+10
    font = 'sans-serif'
    text = 'MASTERMIND'
    shadow_offset = 3
    x = CODE_PADDING
    y = CODE_PADDING
    canvas.create_text(
        CODE_PADDING+shadow_offset,
        CODE_PADDING+shadow_offset,
        text=text,
        font=font,
        font_size = font_size,
        color='#BDBDBD')         
    canvas.create_text(
        CODE_PADDING,
        CODE_PADDING,
        text=text,
        font=font,
        font_size = font_size,
        color='black')     

def display_difficulty(canvas, difficulty):
    """
    Render difficulty info
    """
    x = CANVAS_WIDTH - 100
    y = CODE_PADDING
    text = "mode: "
    if difficulty == 2:
        text += "MEDIUM"
    elif difficulty == 3:
        text += "HARD"
    elif difficulty == 4:
        text += "EXPERT"        
    else:
        text += "EASY"
    draw_info_text(canvas, x, y, text)

def display_info(canvas, has_duplicates):
    """
    Render game play information at bottom of the screen
    """
    x = CODE_PADDING
    y = CANVAS_HEIGHT - (CODE_SIZE+CODE_PADDING)

    # Draw line
    canvas.create_line(0, y, CANVAS_WIDTH, y, 'black')

    # Add exact match info
    x = CODE_PADDING
    y += CODE_PADDING
    canvas.create_oval(x, y, x+KEY_SIZE, y+KEY_SIZE, KEY_EXACT_COLOR, 'black')

    x += KEY_SIZE + 2*KEY_PADDING
    draw_info_text(canvas, x, y, "EXACT MATCH")

    # Add partial match info
    x += CODE_PADDING + 100
    canvas.create_oval(x, y, x+KEY_SIZE, y+KEY_SIZE, KEY_PARTIAL_COLOR, 'black')

    x += KEY_SIZE + 2*KEY_PADDING
    draw_info_text(canvas, x, y, "PARTIAL MATCH")

    # Add duplicate info   
    y -= 2*KEY_PADDING 
    x += CODE_PADDING + 100
    text = "NO DUPLICATES"
    if has_duplicates:
        text = "DUPLICATES ALLOWED"
    draw_info_text(canvas, x, y, text)

    # Add blanks info
    text = "NO BLANKS"
    y += CODE_PADDING
    draw_info_text(canvas, x, y, text)    
  
def draw_info_text(canvas, x, y, text):
    """
    Render information text
    """
    font_size = 12
    font = 'sans-serif'
    font_padding = 2

    canvas.create_text(
        x, 
        y+font_padding, 
        text=text,
        font=font,
        font_size = font_size,
        color='black')        

def play_mastermind(canvas, difficulty, has_duplicates):
    """
    Play the game of mastermind
    - EASY = 12 tries, 6 colors
    - MEDIUM = 10 tries, 7 colors
    - HARD = 8 tries, 9 colors
    - EXPERT = 6 code sequence, 10 tries, 9 colors
    """
    # Update the configuration
    max_guesses = MAX_GUESSES
    colors = COLORS
    num_pegs = NUM_CIRCLES
    if difficulty == 2:
        # Medium mode
        max_guesses = MAX_GUESSES - 2
        colors = COLORS + MEDIUM_COLORS 
    elif difficulty == 3:
        # Hard mode
        max_guesses = MAX_GUESSES - 4
        colors = COLORS + HARD_COLORS 
    elif difficulty == 4:
        # Expert mode
        num_pegs = 6
        max_guesses = MAX_GUESSES
        colors = COLORS + HARD_COLORS         

    # Create the code
    if has_duplicates:
        truth = [random.choice(colors) for _ in range(num_pegs)]
    else:
        truth = random.sample(colors, num_pegs)
    #print(truth)
    is_winner = False

    # Create the guess rows
    guesses = []
    x = CODE_PADDING + CODE_SIZE + 2*CODE_PADDING
    y = CODE_PADDING + CODE_SIZE + CODE_PADDING
    for i in range(max_guesses):
        guess = Guess(canvas, x, y + i*(CODE_SIZE+CODE_PADDING), num_pegs)
        guess.render(canvas)
        guesses.append(guess)
        time.sleep(0)

    # Create color picker
    x = CODE_PADDING
    y = CODE_PADDING + CODE_SIZE + CODE_PADDING
    color_picker = ColorPicker(canvas, x, y, colors)
    color_picker.render(canvas)

    # Play the game
    for i in range(max_guesses):
        # Show button for active row
        guesses[i].show_button(canvas)
        is_winner = play_row(canvas, guesses[i], color_picker, truth)
        
        if is_winner:
            break

    # Done!
    game_over(canvas, truth, is_winner, num_pegs)    

def update_canvas(canvas):
    """
    Call update canvas for non-CIP IDE
    """
    global _is_cip
    if not _is_cip:
        canvas.update()

def main():
    """
    Main method
    """
    # Setup
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    if hasattr(canvas, 'canvas'):
        global _is_cip
        _is_cip = True

    display_header(canvas)
    
    # User settings
    settings = GameSettings()
    settings.render(canvas)
    settings.handle_config(canvas)

    difficulty = settings.difficulty
    has_duplicates = settings.has_duplicates

    # Clear the configuration page
    canvas.clear()
    
    # Display info
    display_header(canvas)
    display_difficulty(canvas, difficulty)
    display_info(canvas, has_duplicates)

    # Play the game
    print("Starting game (Mode: {}) (Allow duplicates: {})".format(difficulty, has_duplicates))
    play_mastermind(canvas, difficulty, has_duplicates)

    # wait for the user to close the window
    if not _is_cip:
        canvas.mainloop()        

if __name__ == '__main__':
    main()
