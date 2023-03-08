
import random
from checkers import Board, Game, Piece
import math
from copy import deepcopy
import click
from colorama import Fore, Style


class RandomBot:
    """
    Class representing the random bot
    """
    def __init__(self, game : Game, color : str):
        """
        Constructor

        Args:
            game(Game): the current game
            color (str): color of bot's pieces
        """
        self._game = game
        self._board = self._game.board
        self._color = color
        self.wins = 0

    def suggest_move(self) -> tuple:
        """
        Suggets a move.

        Returns:
            tuple(Piece, tuple): tuple of the piece that should be moved, and
            where it should be moved to
        """
        all_moves = self._game.player_all_moves(self._board, self._game.current_player)
        rand = random.choice(all_moves)
        _,move,piece = rand
        return piece, move

class SmartBot:
    """
    Class representing the smartbot
    """

    def __init__(self, game : Game, color : str):
        """
        Constructor

        Args:
            game (Game): the current game
            color (str): color of bot's pieces
        """
        self._game = game
        self._board = self._game.board
        self._color = color
        self.wins = 0

    def suggest_move(self) -> tuple:
        """
        Suggests a move!

        Returns:
            tuple(Piece, tuple): a tuple containing the piece that should be
            moved and where it should be moved in coordinate form
        """

        _, best_move = self._minimax(self._board, 2, True, self._game)


        piece, move = best_move
        #print(f"I suggest this move: {piece.location} to {move[0] + 1, move[1] + 1}")

        return piece, move

    def _minimax(self, board_state : Board, depth : int, max_player : bool, game : Game):
        """
        Private method for finding the best move for the smartbot.

        Args:
            board_position (Board): current state of the board
            depth (int): the depth of the game tree
            max_player (bool): whether this is the max player or not
            game (Game): current game

        Returns:
            _type_: _description_
        """


        if depth == 0 or game.end_game:
            return board_state._evaluate(), board_state

        best_move = None
        if max_player: #if AI
            best = -math.inf
            all_moves = self.get_all_moves(board_state, "B", game) #get all of the simulated moves
            for piece,move,new_board in all_moves:
                eval, _ = self._minimax(new_board, depth - 1, False, game)
                if eval > best:
                    best = eval
                    best_move = (piece, move)

        else: #if random or human
            best = math.inf
            all_moves = self.get_all_moves(board_state, "R", game)
            for piece, move, new_board in all_moves:
                eval, _ = self._minimax(new_board, depth - 1, True, game)
                if eval < best:
                    best = eval
                    best_move = (piece, move)

        return best, best_move


    def simulate_move(self, piece, move, board, game):

        ##CANNOT MODIFY GAME VARIABLE!!!!!#####
        ###CHANGE BOARD DIRECTLY####
        ###ALL MOVES INPUTTED WILL BE VALID####
        ###JUST HAVE TO HANDLE JUMPS AND KINGS####

        original_loc = piece.location
        start_row, start_col = piece.location
        end_row, end_col = move

        #are there jumps for the move we're considering?
        jumps = game.piece_all_jumps(piece)
        jumped_piece = None

        #find the piece that the specified move will jump over
        if jumps:
            jumped_piece = board.get_piece_between(piece.location, move)

            #if there is a jumped piece, remove it
            if jumped_piece:
                row, col = jumped_piece.location
                board.grid[row][col] = None
        game.jump_bool = False

        #MOVE THE PIECE!

        board.grid[start_row][start_col] = None
        board.grid[end_row][end_col] = piece
        board.pieces[piece.color].append(piece)


        #handle kings
        if not piece.is_king:
            if (piece.color == 'R' and end_row == board.size - 1) or \
            (piece.color == 'B' and end_row == 0):
                piece.became_king = True
                piece.is_king = True


        new_board = deepcopy(board)

        # REVERSE THE MOVE!


        board._reverse_move(move, original_loc, game, jumped_piece)


        return new_board


    def get_all_moves(self, board, color, game):
        #get all possible moves that we can make from a board
        moves = []
        all_moves = game.player_all_moves(board, color)

        #print(f"all moves redunancy check: {all_moves}")
        for _,move,piece in all_moves:
            #simulate the movement of the piece on the board
            new_board = self.simulate_move(piece, move, board, game)
            moves.append((piece, move, new_board))
        return moves


##SIMULATION
def print_board(board: Board, selected = (-1,-1), pos = [(-1,-1)]) -> None:
    """
    Prints the current state of the board.
    Red pieces are RED
    Black pieces are BLACK
    selected piece is BLUE
    possible move locations are GREEN
    Parameters:
        board(Board): The board that we are printing
        selected(tuple[int,int]): The piece currently selected.
        pos(list[tuple(int,int)]): A list of possible destinations for selected
    """
    # length = board.length
    # width = board.width
    # setting board width and length to 8
    # board
    width, length = board.size, board.size
    c1 = ' '
    for c in range(width):
        if c + 1 < 10:
            c1 += " "
        c1 += "  " + str(c + 1)
    print(Fore.YELLOW + Style.NORMAL + c1)
    print(Fore.YELLOW + Style.NORMAL + "  ┌───" + (width - 1 ) * "┬───" + "┐")
    for r in range(length):
        row = Fore.YELLOW + Style.NORMAL + str(r + 1)
        if len(str(r+1)) == 1:
            row += " │"
        else:
            row += "│"
        for c in range(width):
            square = board.grid[r][c]
            fore = None
            if (r,c)== selected:
                # makes selected piece blue
                fore = Fore.BLUE
            if (r,c) in pos:
                row += Fore.GREEN + ' █ '
            elif type(square) is not Piece:
                if not fore:
                    fore = Fore.BLACK
                row += fore + '   '
            else:
                if square.color == "B" and not fore:
                    fore = Fore.BLACK
                elif square.color == "R" and not fore:
                    fore = Fore.RED
                if square.is_king == True:
                    row += fore + Style.BRIGHT + " K "
                else:
                    row += fore + Style.BRIGHT + " ● "
            row += Fore.YELLOW + Style.NORMAL + "│"
        print(row)
        if r < length - 1:
            print("  ├───" + (width - 1 ) * "┼───" + "┤")
    print("  └───" + (width - 1) * "┴───" + "┘")
    print(Style.RESET_ALL)

class BotPlayer:

    def __init__(self, name, color, game):
        self.name = name
        if self.name == "random":
            self.bot = RandomBot(game, color)
        elif self.name == "smart":
            self.bot = SmartBot(game, color)

        self.color = color
        self.wins = 0

def simulate(player1, player2, num_games, board):
    black_wins = 0
    red_wins = 0

    starting_players = []
    for i in range(num_games):
        print(f"starting game {i}")
        board.reset_board()
        game = Game(board) #current player starts as Black
        if i != 0:
            if starting_players[-1] == "B":
                game.current_player = "R"
            else:
                game.current_player = "B"

        starting_players.append(game.current_player)
        #print(f"{game.current_player} starting this game")
        #print_board(game.board)
        bot1 = BotPlayer(player1, "B", game)
        bot2 = BotPlayer(player2, "R", game)
        bots = {"B": bot1, "R": bot2}
        while not game.end_game:
            piece, move = bots[game.current_player].bot.suggest_move() if bots[game.current_player].bot.suggest_move() != None else None
            #print(f'bot suggests move: {piece.location} to {move}')
            row, col = piece.location
            if move != None:
                game.move(piece, move)#alternates the turn
                #print_board(game.board)


            #print(f"move made: {row, col} to {move[0], move[1]}")
            #print_board(game.board)

        if game.winner is not None:
            #print(f"{game.winner} wins!")
            if game.winner == "B":
                black_wins += 1
            else:
                red_wins += 1
        #print(f"game {i} over")

    #calculate wins

    print(f"'B'({bots['B'].name}) is: {(black_wins/num_games) * 100} %")
    print(f"'R' bot ({bots['R'].name}) is: {(red_wins/num_games) * 100} %")


#check randombot against randombot
#board = Board(6)
#print('testing random against random')
#simulate("random", "random", 10000, board)

#check smart against random
board = Board(6)
print('testing smart against random')
simulate("smart", 'random', 100, board)
