from graphics import Canvas
import random
import time

NUM_CIRCLES = 4
#MAX_GUESSES = 12
MAX_GUESSES = 10

CODE_SIZE = 35
CODE_PADDING = 20
KEY_SIZE = 16
KEY_PADDING = 4
KEY_EXACT_COLOR = 'red'
KEY_PARTIAL_COLOR = 'grey'
BUTTON_WIDTH = 70
BUTTON_HEIGHT = CODE_SIZE

COLORS = ['red', 'orange', '#FEF250', 'green', 'blue', 'purple']
EMPTY_FILL_COLOR = 'white'
OUTLINE_COLOR = 'black'

CANVAS_WIDTH = 500
CANVAS_HEIGHT = (MAX_GUESSES+2) * (CODE_SIZE+CODE_PADDING) + CODE_PADDING
DELAY = 0.1

class ColorPicker:
    def __init__(self, canvas, x, y):
        self.left_x = x
        self.top_y = y
        self.colors = {}
        self.dragger = None
        self.selected_color = None

    def setup(self, canvas):
        """
        Draw the color swatches
        """
        for i in range(len(COLORS)):
            self.colors[canvas.create_oval(
                self.left_x,
                self.top_y + i*(CODE_SIZE+CODE_PADDING),
                self.left_x + CODE_SIZE,
                self.top_y + i*(CODE_SIZE+CODE_PADDING) + CODE_SIZE,
                COLORS[i]
            )] = COLORS[i]

        # Create color dragger
        self.dragger = canvas.create_oval(
            -100,
            -100,
            -100 + CODE_SIZE,
            -100 + CODE_SIZE,
            'white'
        )
    
    def update(self, canvas, x, y):
        canvas.moveto(
            self.dragger, 
            x - CODE_SIZE/2, 
            y - CODE_SIZE/2
        )

    def set_color(self, canvas, selected_color):
        self.selected_color = selected_color
        canvas.set_color(self.dragger, selected_color)

    def reset(self, canvas):
        self.selected_color = None
        canvas.moveto(self.dragger, -100, -100)


class Guess:

    def __init__(self, canvas, x, y):
        self.left_x = x
        self.top_y = y
        self.guesses = ['' for _ in range(NUM_CIRCLES)]
        self.codes = []        
        self.button = None
        self.button_label = None

    def setup(self, canvas):
        """
        Draw the code pegs and key pegs
        """
        # Draw the code pegs
        for i in range(NUM_CIRCLES):
            self.codes.append(canvas.create_oval(
                self.left_x + i*(CODE_SIZE+CODE_PADDING),
                self.top_y,
                self.left_x + i*(CODE_SIZE+CODE_PADDING) + CODE_SIZE,
                self.top_y +CODE_SIZE,
                EMPTY_FILL_COLOR,
                OUTLINE_COLOR
            ))

        # Update
        canvas.update()         

    def _render_keys(self, canvas, colors):
        """
        Render the feedback key pegs
        """
        # Draw the key pegs
        x = self.left_x + (CODE_SIZE+CODE_PADDING)*NUM_CIRCLES
        color_index = 0
        for i in range(NUM_CIRCLES//2):
            for j in range(NUM_CIRCLES//2):
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
        canvas.update() 

    def _render_button(self, canvas):
        """
        Render the check button
        """
        # Draw the Check button
        x = self.left_x + (CODE_SIZE+CODE_PADDING)*NUM_CIRCLES
        self.button = canvas.create_rectangle(
            x,
            self.top_y,
            x + BUTTON_WIDTH,
            self.top_y + BUTTON_HEIGHT,
            EMPTY_FILL_COLOR,
            OUTLINE_COLOR
        )

        # Draw the label
        label = "Check"
        font_size = 16
        font = 'sans-serif'
        padding = 10
        self.button_label = canvas.create_text(
            x + padding,
            self.top_y + padding,
            label,
            font_size = font_size,
            font = font,
            color = OUTLINE_COLOR
        )

        # Update
        canvas.update()         

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

        # Update
        canvas.update()         


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
        for i in range(NUM_CIRCLES):
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
        canvas.delete(self.button)
        canvas.delete(self.button_label)
        self.button = None
        self.button_label = None

        # Render the key pegs
        peg_colors = [ EMPTY_FILL_COLOR for _ in range(NUM_CIRCLES)]
        for i in range(len(key_matches)):
            peg_colors[i] = key_matches[i]
        self._render_keys(canvas, peg_colors)

        # Update
        canvas.update()    
        
        return self.guesses == truth



def game_over(canvas, truth, is_winner):
    """
    Show appropriate game over message
    """
    print("GAME OVER!", is_winner)
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
    truth_x = NUM_CIRCLES*CODE_SIZE
    truth_y = y + font_size + padding
    for i in range(NUM_CIRCLES):
        canvas.create_oval(
            truth_x + i*(CODE_SIZE + CODE_PADDING),
            truth_y,
            truth_x + i*(CODE_SIZE + CODE_PADDING) + CODE_SIZE,
            truth_y + CODE_SIZE,
            truth[i],
            'black'
        )

    # Update
    canvas.update()         

def get_overlapping(canvas):
    """
    Return list of shapes located at last mouse click
    Returns [] if no clicks
    """
    clicks = canvas.get_new_mouse_clicks()
    if clicks:
        # [graphics.py]
        last_click_x = clicks[-1].x
        last_click_y = clicks[-1].y
        overlapping_list = canvas.find_overlapping(
            last_click_x, last_click_y, last_click_x, last_click_y)
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

        # Animation
        if selected_color:
            color_picker.update(canvas, canvas.get_mouse_x(), canvas.get_mouse_y())        

        overlapping_list = get_overlapping(canvas)
        if overlapping_list:
            for overlapping in overlapping_list:
                if overlapping == guess.button:
                    # Clicked on Check button
                    is_correct = guess.check(canvas, truth)
                    is_done = True
                    selected_color = None
                    color_picker.reset(canvas)

                elif selected_color is None and overlapping in color_picker.colors.keys():
                    # Clicked on color picker
                    selected_color = color_picker.colors[overlapping]                    
                    color_picker.set_color(canvas, selected_color)

                elif overlapping == color_picker.dragger:
                    # Ignore mouse dragger
                    pass
                elif selected_color and overlapping in guess.codes:
                    # Clicked on code peg
                    guess.set_guess(canvas, overlapping, selected_color)
                    selected_color = None
                    color_picker.reset(canvas)

        # Sleep
        canvas.update() 
        time.sleep(DELAY)
        
    return is_correct

def display_header(canvas):
    """
    Render the heading
    """
    font_size = CODE_SIZE
    font = 'sans-serif'
    text = 'MASTERMIND'
    x = CODE_PADDING
    y = CODE_PADDING
    canvas.create_text(
        CODE_PADDING,
        CODE_PADDING,
        text=text,
        font=font,
        font_size = font_size,
        color='black') 
    
    # Update
    canvas.update() 

def display_info(canvas):
    """
    Render game play information at bottom of the screen
    """
    x = CODE_PADDING
    y = (MAX_GUESSES+1) * (CODE_SIZE+CODE_PADDING) + CODE_PADDING

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
    x += CODE_PADDING + 100
    draw_info_text(canvas, x, y, "NO DUPLICATES")

    # Update
    canvas.update()          
  
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

def main():
    """
    Main method
    """

    # Setup
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    display_info(canvas)
    display_header(canvas)

    # Create the code
    truth = random.sample(COLORS, 4)
    #print(truth)
    is_winner = False

    # Create the guess rows
    guesses = []
    x = CODE_PADDING + CODE_SIZE + 2*CODE_PADDING
    y = CODE_PADDING + CODE_SIZE + CODE_PADDING
    for i in range(MAX_GUESSES):
        guess = Guess(canvas, x, y + i*(CODE_SIZE+CODE_PADDING))
        guess.setup(canvas)
        guesses.append(guess)

    # Create color picker
    x = CODE_PADDING
    y = CODE_PADDING + CODE_SIZE + CODE_PADDING
    color_picker = ColorPicker(canvas, x, y)
    color_picker.setup(canvas)

    # Play the game
    for i in range(MAX_GUESSES):

        # Show button for active row
        guesses[i].show_button(canvas)
        is_winner = play_row(canvas, guesses[i], color_picker, truth)
        
        if is_winner:
            break

    # Done!
    game_over(canvas, truth, is_winner)

    # wait for the user to close the window
    canvas.mainloop()    

    """
    4 circles
    12 rows (or 6, 8, 10)
    6 colors
    by default, no duplicates
    red dot = correct color and position
    white = correct color but wrong position
    code pegs
    key pegs
    extensions:
    - allow duplicates
    - mobile friendly

    """

if __name__ == '__main__':
    main()
