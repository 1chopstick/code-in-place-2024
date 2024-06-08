from graphics import Canvas
import random
import time

NUM_CIRCLES = 4
MAX_GUESSES = 12

CODE_SIZE = 35
CODE_PADDING = 20
KEY_SIZE = 16
KEY_PADDING = 4
BUTTON_WIDTH = 70
BUTTON_HEIGHT = CODE_SIZE

COLORS = ['red', 'orange', '#FEF250', 'green', 'blue', 'purple']

CANVAS_WIDTH = 500
CANVAS_HEIGHT = (MAX_GUESSES) * (CODE_SIZE+CODE_PADDING) + CODE_PADDING
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
        print(key_matches)
        for i in range(len(key_matches)):
            print(i)
            self.canvas.set_color(self.keys[i], key_matches[i])

        # Update
        self.canvas.update()            
        
        return self.guesses == truth

def game_over(canvas, is_winner):
    """
    Show appropriate game over message
    """
    print("GAME OVER!", is_winner)
    x = 100
    y = CANVAS_HEIGHT/2
    font_size = 50
    text = "GAME OVER"
    if is_winner:
        text = "YOU WIN!"
        x = 130
    
    canvas.create_rectangle(
        0, y, CANVAS_WIDTH, y+font_size, 'white'
    )
    canvas.create_text(
        x,
        y,
        text = text,
        font_size = font_size,
        color = 'black'
    ) 

    # Update
    canvas.update()    

def play_row(canvas, guess, color_picker, truth):
    is_correct = False
    is_done = False
    selected_color = None

    """
    Options:
    1. Pick a new color
    2. Set color of Code peg
    3. Click Check button
    """    
    while not is_done:

        # Select a color
        canvas.wait_for_click()
        click = canvas.get_last_click()
        if click:
            mouse_x, mouse_y = click      
            overlapping_color = canvas.find_overlapping(
                mouse_x, mouse_y, mouse_x, mouse_y
            )

            # Act on Color Picker or Button
            if overlapping_color:
                for obj in overlapping_color:
                    if obj == guess.button:
                        # Check button
                        #print("Clicked Check button")
                        is_correct = guess.check(truth)
                        is_done = True
                    elif obj in color_picker.colors.keys():
                        selected_color = color_picker.colors[overlapping_color[0]]
                        #print("Selected color:", selected_color)
                        color_picker.set_color(selected_color)
                        
                        while True:
                            color_picker.update(canvas.get_mouse_x(), canvas.get_mouse_y())
                            clicks = canvas.get_new_mouse_clicks()
                            if clicks:
                                # [CIP]
                                last_click_x = clicks[-1].x
                                last_click_y = clicks[-1].y
                                overlapping_list = canvas.find_overlapping(
                                    last_click_x, last_click_y, last_click_x, last_click_y)
                                
                                # Act on Code or Button
                                if overlapping_list:
                                    for overlapping in overlapping_list:
                                        if overlapping == color_picker.dragger:
                                            # Ignore
                                            pass
                                        elif overlapping in guess.codes:
                                            # Code peg selected
                                            guess.set_guess(overlapping, selected_color)
                                            break
                                        elif overlapping == guess.button:
                                            # Check button
                                            print("Clicked Check button")
                                            is_correct = guess.check(truth)
                                            is_done = True
                                            break
                                        else:
                                            break
                                color_picker.reset()
                                break 

                            # Sleep
                            time.sleep(DELAY)    
                            canvas.update() 

    return is_correct

def main():
    """
    Main method
    """
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    # Create the code
    truth = random.sample(COLORS, 4)
    print(truth)
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
    game_over(canvas, is_winner)

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
