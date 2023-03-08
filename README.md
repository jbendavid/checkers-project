# project-jbendavid-mbroening-jadotte-kabelo

## Checkers

Members and roles:

- Max Broening: Game Logic
- Jared Bendavid:  Bot
- KB Tsiane:  GUI
- Ashton Jadotte: TUI

This repository contains a design and implementation of the game of checkers.

### Running the TUI

To run the TUI, run the following from the root of the repository:

- python3 src/tui.py
- Then input your choices for player1, type player2 type, bot delay, and board size
- With the three type options "human", "random", and "smart".
- The bot delay is the delay between bots making a move and can be any int/tuple >= 0.
- The board size can be any int between and including 6 and 20.
- The default if player 1 is human and player 2 is a random bot.
- After this you will be prompted to input a board size valid sizes range from 6-20.
- Finally you will be prompted to input the number of rounds you would like to play, you can add an extra round after each game. Keep at default if a human is playing. This only exists for running bots against eachother in large batches.
- Moves must be inputed by selecting a square in the format row,column and then selecting the square to move that piece in the same format.
- A draw can be offered by inputing "draw", bots will always reject draws
- You can resign by inputing "I resign"
- After each game has ended the running score between player 1 and player 2 will be printed
- Each player will then be prompted if they would like a rematch. Both players must accept for a rematch to occur.

So far human and random bots have been integrated

### Running the GUI

To run the GUI, run the following from the root of the repository:
python3 src/gui.py
This will display a 6x6 checkers board with red and black pieces.

### Bots

The simulation for running the random bot against the smart bot is
not yet fully developed. In the bots.py file, you will find a crude
representation of how this might work. The checkers_sim function, while not yet
finished, will accomplish the simulation.
