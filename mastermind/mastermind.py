from graphics import Canvas
import random
import time

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

CANVAS_WIDTH = 500
CANVAS_HEIGHT = (MAX_GUESSES+1) * (CODE_SIZE+CODE_PADDING) + CODE_PADDING
DELAY = 0.1

class ColorPicker:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.left_x = x
        self.top_y = y
        self.colors = {}
        self.dragger = None
        self.selected_color = None
        self._setup()

    def _setup(self):
        """
        Draw the color swatches
        """
        for i in range(len(COLORS)):
            self.colors[self.canvas.create_oval(
                self.left_x,
                self.top_y + i*(CODE_SIZE+CODE_PADDING),
                self.left_x + CODE_SIZE,
                self.top_y + i*(CODE_SIZE+CODE_PADDING) + CODE_SIZE,
                COLORS[i]
            )] = COLORS[i]

        # Create color dragger
        self.dragger = self.canvas.create_oval(
            -100,
            -100,
            -100 + CODE_SIZE,
            -100 + CODE_SIZE,
            'white'
        )
    
    def update(self, x, y):
        self.canvas.moveto(
            self.dragger, 
            x - CODE_SIZE/2, 
            y - CODE_SIZE/2
        )

    def set_color(self, selected_color):
        self.selected_color = selected_color
        self.canvas.set_color(self.dragger, selected_color)

    def reset(self):
        self.selected_color = None
        self.canvas.moveto(self.dragger, -100, -100)


class Guess:

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.left_x = x
        self.top_y = y
        self.guesses = ['' for _ in range(NUM_CIRCLES)]
        self.codes = []
        self.keys = []
        self.button = None
        self.button_label = None
        self.is_locked = False
        self._setup()

    def _setup(self):
        """
        Draw the code pegs and key pegs
        """

        fill = 'white'
        outline = 'black'

        # Draw the code pegs
        for i in range(NUM_CIRCLES):
            self.codes.append(self.canvas.create_oval(
                self.left_x + i*(CODE_SIZE+CODE_PADDING),
                self.top_y,
                self.left_x + i*(CODE_SIZE+CODE_PADDING) + CODE_SIZE,
                self.top_y +CODE_SIZE,
                fill,
                outline
            ))

        # Draw the key pegs
        x = self.left_x + (CODE_SIZE+CODE_PADDING)*NUM_CIRCLES
        for i in range(NUM_CIRCLES//2):
            for j in range(NUM_CIRCLES//2):
                self.keys.append(self.canvas.create_oval(
                    x + j*(KEY_SIZE+KEY_PADDING),
                    self.top_y + i*(KEY_SIZE+KEY_PADDING),
                    x + j*(KEY_SIZE+KEY_PADDING) + KEY_SIZE,
                    self.top_y + i*(KEY_SIZE+KEY_PADDING) + KEY_SIZE,
                    fill,
                    outline
                ))   

        # Draw the check button
        #x += 2*(KEY_SIZE+KEY_PADDING) + CODE_PADDING
        x = self.left_x + (CODE_SIZE+CODE_PADDING)*NUM_CIRCLES
        self.button = self.canvas.create_rectangle(
            x,
            self.top_y,
            x + BUTTON_WIDTH,
            self.top_y + BUTTON_HEIGHT,
            fill,
            outline
        )

        # Draw the label
        label = "Check"
        font_size = 16
        font = 'sans-serif'
        padding = 10
        self.button_label = self.canvas.create_text(
            x + padding,
            self.top_y + padding,
            label,
            font_size = font_size,
            font = font,
            color = outline
        )

        # Hide controls
        self.hide_button()
        self._toggle_keys(True)

    def _toggle_keys(self, is_hidden):
        for key in self.keys:
            self.canvas.set_hidden(key, is_hidden)

        # Update
        self.canvas.update()
        
    def hide_button(self):
        """
        Hide the 'Check' button
        """
        # Hide button
        self.canvas.set_hidden(self.button_label, True)
        self.canvas.set_hidden(self.button, True)

        # Show keys
        self._toggle_keys(False)

        # Update
        self.canvas.update()

    def show_button(self):
        """
        Show the 'Check' button
        """
        # Show button
        self.canvas.set_hidden(self.button_label, False)
        self.canvas.set_hidden(self.button, False)

        # Hide keys
        self._toggle_keys(True)

        # Update
        self.canvas.update()

    def set_guess(self, code, color):

        for i in range(len(self.codes)):
            if code == self.codes[i]:
                self.guesses[i] = color

        # Update the color
        self.canvas.set_color(code, color)
        #print("Current guess:", self.guesses)

        # Update
        self.canvas.update()        


    def check(self, truth):
        """
        Update the key pegs and return True if the Code pegs matches the truth list
        - red key means color and position is correct
        - grey key means color is correct but position is incorrect
        """

        # Compare color of key pegs to truth
        exact_color = 'red'
        partial_color = 'grey'
        key_matches = []
        key_index = 0
        unmatched_indices = []
        unmatched_truth = []

        # Check for exact matches
        for i in range(NUM_CIRCLES):
            if self.guesses[i] == truth[i]:
                key_matches.append(exact_color)
            else:
                unmatched_indices.append(i)
                unmatched_truth.append(truth[i])

        # Check for partial matches
        for i in unmatched_indices:
            if self.guesses[i] in unmatched_truth:
                key_matches.append(partial_color)
                unmatched_truth.remove(self.guesses[i])

        # Update the key graphics
        for i in range(len(key_matches)):
            self.canvas.set_color(self.keys[i], key_matches[i])

        # Update
        self.canvas.update()            
        
        return self.guesses == truth


def display_info(canvas):
    """
    Show game play information at bottom of the screen
    """
    x = CODE_PADDING
    y = (MAX_GUESSES) * (CODE_SIZE+CODE_PADDING) + CODE_PADDING

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

def game_over(canvas, truth, is_winner):
    """
    Show appropriate game over message
    """
    print("GAME OVER!", is_winner)
    x = 100
    y = CODE_PADDING + CODE_SIZE + CODE_PADDING - 5
    font_size = 50
    text = "GAME OVER"
    if is_winner:
        text = "YOU WIN!"
        x = 130
    
    canvas.create_rectangle(
        0, y, CANVAS_WIDTH, y+font_size+CODE_SIZE+CODE_PADDING, 'white'
    )
    canvas.create_text(
        x,
        y,
        text = text,
        font_size = font_size,
        color = 'black'
    )   

    # Show solution
    truth_x = NUM_CIRCLES*CODE_SIZE
    truth_y = y + font_size
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
            color_picker.update(canvas.get_mouse_x(), canvas.get_mouse_y())        

        overlapping_list = get_overlapping(canvas)
        if overlapping_list:
            for overlapping in overlapping_list:
                if overlapping == guess.button:
                    # Clicked on Check button
                    is_correct = guess.check(truth)
                    is_done = True
                    selected_color = None
                    color_picker.reset()
                    #print("Check button")
                elif selected_color is None and overlapping in color_picker.colors.keys():
                    # Clicked on color picker
                    selected_color = color_picker.colors[overlapping]                    
                    color_picker.set_color(selected_color)
                    #print("Selected color:", selected_color)
                elif overlapping == color_picker.dragger:
                    # Ignore mouse dragger
                    pass
                elif selected_color and overlapping in guess.codes:
                    # Clicked on code peg
                    guess.set_guess(overlapping, selected_color)
                    selected_color = None
                    color_picker.reset()

        # Sleep
        canvas.update() 
        time.sleep(DELAY)
        
    return is_correct

def main():
    """
    Main method
    """
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    display_info(canvas)

    # Create the code
    truth = random.sample(COLORS, 4)
    #print(truth)
    is_winner = False

    # Create the guess rows
    guesses = []
    x = CODE_PADDING + CODE_SIZE + 2*CODE_PADDING
    y = CODE_PADDING
    for i in range(MAX_GUESSES):
        guesses.append(Guess(canvas, x, y + i*(CODE_SIZE+CODE_PADDING)))

    # Create color picker
    x = CODE_PADDING
    y = CODE_PADDING
    #y = (MAX_GUESSES) * (CODE_SIZE+CODE_PADDING) + CODE_PADDING
    color_picker = ColorPicker(canvas, x, y)

    # Play the game
    for i in range(MAX_GUESSES):

        # Show button for active row
        guesses[i].show_button()
        is_winner = play_row(canvas, guesses[i], color_picker, truth)
        
        if is_winner:
            break
        else:
            # Hide button for active row
            guesses[i].hide_button()

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
