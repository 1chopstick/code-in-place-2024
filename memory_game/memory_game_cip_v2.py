from graphics import Canvas
import random

MAX_SHAPES = 6
NUM_PAIRS = 6
NUM_ROW = 3
NUM_COLS = 4

CARD_SIZE = 100
PADDING = 10
    
CANVAS_WIDTH = CARD_SIZE * NUM_COLS
CANVAS_HEIGHT = CARD_SIZE * NUM_ROW


class Card:

    RED = '#FA9189'
    ORANGE = '#FCAE7C'
    LITE_ORANGE = '#FFE699'
    YELLOW = '#F9FFB5'
    GREEN = '#B3F5BC'
    BLUE = '#D6F6FF'
    LITE_PURPLE = '#E2CBF7'
    PURPLE = '#D1BDFF'

    def __init__(self, canvas, value):
        self.canvas = canvas
        self.value = value
        self.back = None
        self.front = None
        self.image = None
        self.x = 0
        self.y = 0
        self.is_matched = False

    def create_card(self, x, y):
        self.x = x
        self.y = y
        green = '#abd672'
        #blue = '#7fcce4'
        #pink = '#fe9ca0'
        #yellow = '#38361c'

        # Draw the back of the card
        self.back = self.canvas.create_rectangle(
            self.x+PADDING,
            self.y+PADDING,
            self.x+CARD_SIZE-PADDING,
            self.y+CARD_SIZE-PADDING,
            green,
            'black'
        )

        # Draw the front of the card
        self.front = self.canvas.create_rectangle(
            self.x+PADDING,
            self.y+PADDING,
            self.x+CARD_SIZE-PADDING,
            self.y+CARD_SIZE-PADDING,
            'white',
            'black'
        )

        if self.value == 1:
            self._draw_circle()
        elif self.value == 2: 
            self._draw_hexagon()
        elif self.value == 3:
            self._draw_triangle()
        elif self.value == 4:
            self._draw_square()              
        elif self.value == 5:
            self._draw_pentagon()        
        elif self.value == 6:
            self._draw_rectangle()                   
        else:
            self._draw_diamond()
        self.hide_card()
        
    def show_card(self):
        self.canvas.set_hidden(self.front, False)
        self.canvas.set_hidden(self.image, False)
        self.canvas.set_hidden(self.back, True)


    def hide_card(self):
        self.canvas.set_hidden(self.front, True)
        self.canvas.set_hidden(self.image, True)
        self.canvas.set_hidden(self.back, False)

    def _draw_circle(self):
        color = 'red'
        offset = PADDING*2
        self.image = self.canvas.create_oval(
            self.x + offset,
            self.y + offset,
            self.x+CARD_SIZE-offset,
            self.y+CARD_SIZE-offset,
            color
        )

    def _draw_square(self):
        color = 'blue'
        offset = PADDING*2
        self.image = self.canvas.create_rectangle(
            self.x + offset,
            self.y + offset,
            self.x+CARD_SIZE-offset,
            self.y+CARD_SIZE-offset,
            color
        )

    def _draw_rectangle(self):
        color = 'indigo'
        offset = PADDING*2
        self.image = self.canvas.create_rectangle(
            self.x + offset,
            self.y + offset*2,
            self.x+CARD_SIZE-offset,
            self.y+CARD_SIZE-offset*2,
            color
        )        

    def _draw_triangle(self):
        color = 'green'
        offset = PADDING*2
        self.image = self.canvas.create_polygon(
            self.x+CARD_SIZE/2, self.y+offset,
            self.x+offset, self.y+CARD_SIZE-offset,
            self.x+CARD_SIZE-offset, self.y+CARD_SIZE-offset,
            color=color
        )   

    def _draw_diamond(self):
        color = 'orange'
        offset = PADDING*2
        self.image = self.canvas.create_polygon(
            self.x+CARD_SIZE/2, self.y+offset,
            self.x+offset, self.y+CARD_SIZE/2,
            self.x+CARD_SIZE/2, self.y+CARD_SIZE-offset,
            self.x+CARD_SIZE-offset, self.y+CARD_SIZE/2,
            color=color
        )

    def _draw_hexagon(self):
        color = 'purple'
        offset = PADDING*2
        self.image = self.canvas.create_polygon(
            self.x+CARD_SIZE/3, self.y+offset,
            self.x+offset, self.y+CARD_SIZE/2,
            self.x+CARD_SIZE/3, self.y+CARD_SIZE-offset,
            self.x+CARD_SIZE-CARD_SIZE/3, self.y+CARD_SIZE-offset,
            self.x+CARD_SIZE-offset, self.y+CARD_SIZE/2,
            self.x+CARD_SIZE-CARD_SIZE/3, self.y+offset,
            color=color
        )        

    def _draw_pentagon(self):
        color = '#FEF250'    # Yellow
        offset = PADDING*2
        self.image = self.canvas.create_polygon(
            self.x+CARD_SIZE/2, self.y+offset,
            self.x+offset, self.y+CARD_SIZE/2,
            self.x+CARD_SIZE/3, self.y+CARD_SIZE-offset,
            self.x+CARD_SIZE-CARD_SIZE/3, self.y+CARD_SIZE-offset,
            self.x+CARD_SIZE-offset, self.y+CARD_SIZE/2,
            color=color
        )    

    def _draw_octagon(self):
        pass

    def _draw_trapezoid(self):
        pass

    def _draw_parallelogram(self):
        pass


"""
Return the Card instance that was selected by the mouse
"""
def pick_card(canvas, cards):
    canvas.wait_for_click()
    click = canvas.get_last_click()
    if click:
        mouse_x = click[0]
        mouse_y = click[1]            
        shapes = canvas.find_overlapping(
            mouse_x,
            mouse_y,
            mouse_x,
            mouse_y
        )
        for shape in shapes:
            for card in cards:
                if card.back == shape:
                    return card
    return None

"""
Main
"""
def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    cards = []
    matches = 0
    tries = 0

    # Create the cards
    for i in range(NUM_PAIRS):
        cards.append(Card(canvas, i))
        cards.append(Card(canvas, i))

    # Shuffle the cards
    random.shuffle(cards)

    # Render the cards
    index = 0
    for row in range(NUM_ROW):
        for cols in range(NUM_COLS):
            x = cols*CARD_SIZE
            y = row*CARD_SIZE
            cards[index].create_card(x, y)
            index += 1
    
    # Game loop
    while matches != NUM_PAIRS:
        tries += 1

        # Pick the first card and make sure it's valid
        first_card = pick_card(canvas, cards)
        while not first_card:
            first_card = pick_card(canvas, cards)

        if first_card.is_matched:
            print("This card has already been matched. Try again.")
            continue
        else:
            first_card.show_card()

        # Pick the second card
        second_card = pick_card(canvas, cards)
        while not second_card:
            second_card = pick_card(canvas, cards)

        # Check if they are valid choices
        if first_card == second_card:
            print("You picked the same card twice. Try again.")
            first_card.hide_card()
            continue
        elif second_card.is_matched:
            print("This card has already been matched. Try again.")
            first_card.hide_card()
            continue
        else:
            second_card.show_card()

        # Check if they match
        if first_card.value == second_card.value:
            # Match!
            first_card.is_matched = True
            second_card.is_matched = True
            print("Match!")
            matches += 1
        else:
            # Reset
            print("No match. Try again.")
            time.sleep(1)
            first_card.hide_card()
            second_card.hide_card()
    
    # Game over!
    print("Congratulations! You won! It took you {} tries!".format(tries))


if __name__ == '__main__':
    main()
