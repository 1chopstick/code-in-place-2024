# Mastermind

Play the classic game of Mastermind [here](https://codeinplace.stanford.edu/cip4/share/53kI3TMUXJqWFKNPkVGC).

## Project Proposal

### Milestones

#### Set Up Your Graphics Canvas

Initialize the graphics canvas where game elements will be displayed. Create the basic layout including the rows for guess pegs, the palette for selecting colors, and areas for key pegs.

#### Create Color Palette and Selection Mechanism

Design the color palette with six colors and set up the functionality that allows the player to select a color by clicking on it. Represent the selected color visually and store it for later use.

#### Generate the Secret Code

Write a function that randomly selects four colors from your list of six colors to form the secret code, ensuring there are no duplicates. Store this code in a list for use throughout the game.

#### Track Player Guesses

Design the code pegs where players will click to place their guesses. Implement logic to record the player's selected colors in the appropriate locations. Also, set up a variable to track the number of tries left.

#### Check Guesses and Provide Feedback

Write a function to compare the player's guess to the secret code. Use lists to keep track of which colors are in the correct position and which are the correct color but in the wrong position. Display the feedback using key pegs (red for correct color and position, grey for correct color but wrong position).

#### Display End Game Message

Create the logic to display either a 'You Win' or 'Game Over' message based on whether the player successfully guesses the code or exhausts all their tries. Reveal the secret code when the game ends.

#### Testing and Debugging

Carefully test each part of your game: start with canvas rendering, color selection, guess placement, feedback mechanism, and end-game conditions. Fix any bugs that arise and ensure that the game flows smoothly.

Polish and Extend
If time permits, add enhancements like allowing duplicate colors in the secret code, increasing the number of code pegs, or adding options for more or fewer guesses. You can also look into making the game mobile-compatible.
