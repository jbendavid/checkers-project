# gui for game

import pygame as pg
import click

#constants

HEIGHT = 600
WIDTH = 600
RED = (255,0,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BISQUE = (235, 199, 178)
COFFEE = (103, 71, 54)
YELLOW = (255, 239, 0)

from checkers import Board, Game, Piece
from bots import RandomBot, SmartBot

class GUIPlayer:
    """
    Simple class to store information about a GUI player
    """

    def __init__(self, n: int, player_type: str, board: Board,
                 color: str, game: Game):
        """ Constructor
        Args:
            n: The player's number (1 or 2)
            player_type: "human", "random-bot", or "smart-bot"
            board: The game board
            color: The player's color
            opponent_color: The opponent's color
        """

        if player_type == "human":
            self.name = f"Player {n}"
            self.bot = None
        elif player_type == "smartbot":
            self.name = f"Smart Bot {n}"
            self.bot = SmartBot(game, color)
        elif player_type == "randombot":
            self.name = f'Random Bot {n}'
            self.bot = RandomBot(game, color)

        self.type = player_type
        self.board = board
        self.color = color

        return


def draw_board(surface: pg.surface.Surface, board: Board, moves = None) -> None:
    """
    Draws the current state of the board
    parameters:
        surface: pygame surface to draw the board on
        board: the board to draw
        moves: a piece's available moves
        jumps: a piece's available jumps
    returns: None
    """

    nrows = board.size
    ncols = board.size

    # Compute each cell height and width
    cell_height = HEIGHT // nrows + 1
    cell_width = WIDTH // ncols + 1

    surface.fill(COFFEE)
    # add the lighter squares to the board
    for row in range(nrows):
        for col in range(row%2, ncols, 2):
            rect = (col * cell_width, row * cell_height, cell_width, cell_height)
            pg.draw.rect(surface, color=BISQUE, rect=rect, width=0)

    draw_pieces(surface, board, cell_height, cell_width, moves)

    return

def draw_pieces(surface: pg.surface.Surface, board: Board, cell_height: int, cell_width: int, moves = None) -> None:

    p1pieces = board.pieces['B']
    p2pieces = board.pieces['R']

    radius = min(cell_height//3, cell_width//3)
    for p1 in p1pieces:
        center = (p1.location[0]*cell_width + cell_width//2, p1.location[1]*cell_height + cell_height//2)
        if p1.is_king:
            pg.draw.circle(surface, color=BLACK, center = center, radius=radius)
            pg.draw.circle(surface, color=YELLOW, center = center, radius=radius, width = 3)
        else:
            pg.draw.circle(surface, color=BLACK, center = center, radius=radius)
            
    for p2 in p2pieces:
        center = (p2.location[0]*cell_width + cell_width//2, p2.location[1]*cell_height + cell_height//2)
        if p2.is_king:
            pg.draw.circle(surface, color=RED, center = center, radius=radius)
            pg.draw.circle(surface, color=YELLOW, center = center, radius=radius, width = 3)
        else:
            pg.draw.circle(surface, color=RED, center = center, radius=radius)

    if moves is not None:
        for mx, my in moves:
            center = (mx*cell_width + cell_width//2, my*cell_height + cell_height//2)
            pg.draw.circle(surface, color=BLUE, center = center, radius=radius, width = 3)

    return


def play_game(game: Game, board: Board, players: dict[GUIPlayer],
                bot_delay: float = 2) -> None:
    """
    Plays the game in a pygame window

    parameters:
        game: the game being played
        board: the board the game is being played on
        players: the players
        bot_delay: artifical time delay, in seconds, before the bot makes a move
    """

    pg.init()
    pg.display.set_caption("Checkers")  #need to generalize to the game name
    surface = pg.display.set_mode((HEIGHT, WIDTH))
    clock = pg.time.Clock()

    selected = None
    running = True
    moves = None
    while running:
        current = players[game.current_player]
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif current.bot is None and event.type == pg.MOUSEBUTTONDOWN:
                xx, yy = event.pos
                x = int(xx//(WIDTH/board.size))
                y = int(yy//(HEIGHT/board.size))
                selected = select(game, board, current, selected, x, y)
                if selected is not None:
                    moves = game.piece_all_moves(board, selected)
                else:
                    moves = None
            
        if current.bot is not None:
            pg.time.wait(int(bot_delay * 1000))
            selected, location = current.bot.suggest_move()
            move(game, selected, location[0], location[1])

        draw_board(surface, board, moves)
        pg.display.update()
        clock.tick(24)

def select(game: Game, board: Board, current: str, selected, row: int, col: int):
    """
    Function to make a selection on the board

    parameters:
        game: the game being played
        board: the board being played on
        current: the current player's turn
        selected: the current player's selection which could be a Piece or None
        row: row where mouse was clicked
        col: column where mouse was clicked

    returns: 
        selected: the new selection which could be a Piece or None
    """

    tmp = board.grid[row][col]
    if tmp is not None:
        if tmp.color != current.color:
            print("Not your turn!")
            return None

    if selected is None:
        if tmp is not None:
            selected = tmp

    if selected is not None:
        if tmp is None:
            print('before: ', selected.location)   
            print(game.piece_all_moves(board, selected))
            move(game, selected, row, col)

            print('After: ', selected.location)

            selected = None
        else:
            selected = tmp

    return selected

def move(game: Game, selected: Piece, row: int, col: int) -> None:
    """ 
    Move a piece
    
    parameters:
        game: the game being played
        selected: the piece to be moved
        row: the row the piece is in
        col: the column the piece is in
        
    returns: None"""
    
    try:
        game.move(selected, (row, col))
    except ValueError as err:
        print(err)
    return

@click.command()
#@click.option('--mode', default='real')
@click.option('--player1', default="human", help="The type of player 1 (human, randombot or smartbot)")
@click.option('--player2', default="human", help="The type of player 2 (human, randombot or smartbot)")
@click.option('--size', default=6, help="n x n size of the board")
def cmd(size, player1, player2):
    board = Board(size)
    checkers = Game(board, "R")
    player1 = GUIPlayer(1, player1, board, "B", checkers)
    player2 = GUIPlayer(2, player2, board, "R", checkers)
    players = {player1.color: player1, player2.color: player2}

    play_game(checkers, board, players)

if __name__ == "__main__":
    cmd()
