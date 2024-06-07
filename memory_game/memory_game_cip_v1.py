from graphics import Canvas
import random

NUM_PAIRS = 4
NUM_ROW = 1
NUM_COLS = 8

CARD_SIZE = 100
PADDING = 10
    
CANVAS_WIDTH = CARD_SIZE * NUM_COLS
CANVAS_HEIGHT = CARD_SIZE * NUM_ROW

def draw_card(canvas, x, y):
    """
    Draw the empty card at location (x,y)
    """
    return canvas.create_rectangle(
        x+PADDING,
        y+PADDING,
        x+CARD_SIZE-PADDING,
        y+CARD_SIZE-PADDING,
        'white',
        'black'
    )

def draw_circle(canvas, x, y):
    """
    Draw a circle at location (x,y)
    """
    color = 'red'
    offset = PADDING*2
    return canvas.create_oval(
        x + offset,
        y + offset,
        x+CARD_SIZE-offset,
        y+CARD_SIZE-offset,
        color
    )

def draw_square(canvas, x, y):
    """
    Draw a square at location (x,y)
    """
    color = 'blue'
    offset = PADDING*2
    return canvas.create_rectangle(
        x + offset,
        y + offset,
        x+CARD_SIZE-offset,
        y+CARD_SIZE-offset,
        color
    )

def draw_triangle(canvas, x, y):
    """
    Draw a triangle at location (x,y)
    """
    color = 'green'
    offset = PADDING*2
    return canvas.create_polygon(
        x+CARD_SIZE/2, y+offset,
        x+offset, y+CARD_SIZE-offset,
        x+CARD_SIZE-offset, y+CARD_SIZE-offset,
        color=color
    )

def draw_diamond(canvas, x, y):
    """
    Draw a diamond at location (x,y)
    """
    color = 'purple'
    offset = PADDING*2
    return canvas.create_polygon(
        x+CARD_SIZE/2, y+offset,
        x+offset, y+CARD_SIZE/2,
        x+CARD_SIZE/2, y+CARD_SIZE-offset,
        x+CARD_SIZE-offset, y+CARD_SIZE/2,
        color=color
    )

def create_shape(canvas, value, x, y):
    """
    Return shape corresponding to int value
    """
    if value == 0:
        shape = draw_circle(canvas, x, y)
    elif value == 1: 
        shape = draw_square(canvas, x, y)
    elif value == 2:
        shape = draw_diamond(canvas, x, y)
    else:
        shape = draw_triangle(canvas, x, y)
    return shape

def show_card(canvas, card, display, truth, lookup):
    """
    Show the shape on the card
    """
    shape = None
    index = lookup[card]
    value = truth[index]
    if display[index]:
        # Shape already exist, show it
        canvas.set_hidden(display[index], False)
    else:
        # Need to create the shape
        x = canvas.get_left_x(card) - PADDING
        y = canvas.get_top_y(card) - PADDING
        display[index] = create_shape(canvas, truth[index], x, y)  

def pick_card(canvas, lookup):
    """
    Return the blank card that was selected
    """
    card = None
    canvas.wait_for_click()
    click = canvas.get_last_click()
    if click:
        mouse_x = click[0]
        mouse_y = click[1]            
        cards = canvas.find_overlapping(
            mouse_x,
            mouse_y,
            mouse_x,
            mouse_y
        )
        if cards and cards[0] in lookup.keys():
            return cards[0]
    return card

def flip_card(canvas, display, truth, lookup):
    """
    Show the shape on the selected card
    """
    card = None
    index = -1
    canvas.wait_for_click()
    click = canvas.get_last_click()
    if click:
        mouse_x = click[0]
        mouse_y = click[1]
        cards = canvas.find_overlapping(
            mouse_x,
            mouse_y,
            mouse_x,
            mouse_y
        )
        if cards and cards[0] in lookup:
            # Must click on empty card only, not a shape
            show_card(canvas, cards[0], display, truth, lookup)
            card = cards[0]
    return card

def hide_card(canvas, shape):
    """
    Hide the shape
    """
    canvas.set_hidden(shape, True)


def main():
    """
    Main method
    """
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    truth = []      # List of numbers
    display = []    # List of shape graphic objects
    matched = []    # List of boolean to mark card as already matched
    lookup = {}     # Map list index to card graphic object
    matches = 0     # Number of successful matches
    tries = 0       # Number of unsuccessful matches

    # Milestone #1: Create the truth list
    for i in range(NUM_PAIRS):
        truth.append(i)
        truth.append(i)    

    # Milestone #2: Shuffle the list
    random.shuffle(truth)

    # Milestone #3: Create a displayed list
    # (This syntax is called python list comprehension)
    display = [None for _ in range(NUM_PAIRS*2)]  
    matched = [False for _ in range(NUM_PAIRS*2)] 
    
    # Render the empty cards
    # (Currently only support cards all in one row)
    for row in range(NUM_ROW):
        for cols in range(NUM_COLS):
            x = cols*CARD_SIZE
            y = row*CARD_SIZE
            lookup[draw_card(canvas, x, y)] = cols

    # Play the game    
    while matches != NUM_PAIRS:

        tries += 1

        # Make sure first card is valid
        first_card = pick_card(canvas, lookup)
        while not first_card:
            first_card = pick_card(canvas, lookup)
            
        if matched[lookup[first_card]]:
            print("This card has already been matched. Try again.")
            continue
        else:
            show_card(canvas, first_card, display, truth, lookup)
        
        # Make sure second card is valid
        second_card = pick_card(canvas, lookup)
        while not second_card:
            second_card = pick_card(canvas, lookup)

        # Milestone #5: Check correct
        if first_card == second_card:
            print("You picked the same card twice. Try again.")
            hide_card(canvas, display[lookup[first_card]])
            continue
        elif matched[lookup[second_card]]:
            print("This card has already been matched. Try again.")
            hide_card(canvas, display[lookup[first_card]])
            continue            
        else:
            show_card(canvas, second_card, display, truth, lookup)

        first_index = lookup[first_card]
        second_index = lookup[second_card]

        if truth[first_index] == truth[second_index]:
            # Match!
            matched[first_index] = True
            matched[second_index] = True
            print("Match!")
            matches += 1
        else:
            # Reset
            print("No match. Try again.")
            time.sleep(1)
            hide_card(canvas, display[first_index])
            hide_card(canvas, display[second_index])        

    print("Congratulations! You won! It took you {} tries!".format(tries))

    
if __name__ == '__main__':
    main()
