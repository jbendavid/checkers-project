#Checkers game
class Board:
    """
    Class that generates and represents a game board, establishes piece objects,
    and includes game class to actually play checkers.
    Examples:
    1) Creating a board:
        board = Board(8, 8)
    2) Check move feasability:
        move_valid = Game.is_valid_move(piece_1, (3,4))
    3) All possible piece moves:
        piece_moves = Game.piece_all_moves(board, piece_8)
    4) All possible player moves:
        all_moves = Game.player_all_moves(player1, board)
    5) Check and identify winnner:
        if game.end_game:
	        winner = Game.winner_loser(board)
    """

    def __init__(self, size):
        """
        Constructor
        Args:
            length (int): the length of the board
            width (int): the width of the board
        """

        self.pieces = {'B': [], 'R': []}
        self.red_kings = 0
        self.black_kings = 0
        self.terminal_board = False


        # list[list[Piece]]: the board
        self.grid = [[None for _ in range(size)] for _ in range(size)]

        #int : the number of rows in the board
        self._length = size

        #int : the number of tiles per row
        self._width = size
        self.size = size
        self.reset_board()


    def reset_board(self):
        """
        Method to reset the board to the starting position
        """
        self.empty_board()
        layers = (self.size -2) / 2
        for row in range(self.size):
            for col in range(self.size):
                if row % 2 == col % 2:  # Only add pieces to dark squares
                    if row < layers:  # Add red pieces to the top 3 rows
                        piece = Piece("R", (row, col))
                        self.add_piece(piece)
                    elif row >= self.size - layers:  # Add black pieces to the bottom 3 rows
                        piece = Piece("B", (row, col))
                        self.add_piece(piece)


    def add_piece(self, piece):
        """
        Method to add a piece to the board
        Args:
            piece (Piece object) - piece to add
        Returns:
            None
        """
        row, col = piece.location
        self.grid[row][col] = piece
        self.pieces[piece.color].append(piece)

    def remove_piece(self, piece):
        """
        Method that removes a piece from the board and from the self.pieces
        attribute
        Args:
            piece (Piece object) - piece to remove
        Returns:
            None
        """
        row, col = piece.location
        self.grid[row][col] = None
        self.pieces[piece.color].remove(piece)


    def get_piece(self, location):
        """
        Method that returns the piece object at a location
        Args:
            location (tuple) - location at which to identify piece
        Returns:
            Piece object or None, if no piece at location
        """
        row, col = location
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.grid[row][col]
        else:
            return None

    def get_piece_between(self, start, end):
        """
        Method to get the Piece object between two squares on the board.
        Args:
            start (tuple) - location 1
            end (tuple) - location 2
        Returns:
            The piece on the square between the two locations, if it exists
        """
        x1, y1 = start
        x2, y2 = end
        if abs(x2 - x1) != 2 or abs(y2 - y1) != 2:
            return None  # No piece to remove

        # Determine position of piece between start and end positions
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        mid_pos = (mid_x, mid_y)

        # Get the piece at the middle position
        return self.get_piece(mid_pos)

    def get_all_pieces(self, color : str):
        #print(f"all pieces for {color} are: {self.pieces[color]}")
        return self.pieces[color]

    def empty_board(self) -> None:
        """
        Method that removes all of the pieces on a board.
        """
        for piece in self.pieces["B"]:
            row, col = piece.location
            self.grid[row][col] = None

        for piece in self.pieces["R"]:
            row, col = piece.location
            self.grid[row][col] = None
        self.pieces["B"] = []
        self.pieces["R"] = []

    def _evaluate(self):
        black_left = len(self.pieces["B"])
        red_left = len(self.pieces["R"])
        return black_left - red_left + (self.black_kings * 0.5 - self.red_kings * 0.5)


    def _reverse_move(self, move, original_loc, game, jumped_piece = None):

        # piece -> the piece that was just moved; the one we want to move back
        # original_loc -> the original location of the piece
        #jumps --> pieces jumped during the move that we need to add back


        start_row, start_col = move
        end_row, end_col = original_loc

        #get the piece that moved
        piece_moved = self.get_piece(move)

        #if the piece became a king, unking it


        if piece_moved.became_king:
            piece_moved.is_king = False
            piece_moved.became_king = False


        #return the moved piece back to its original location and empty out the
        #square it moved to

        self.grid[end_row][end_col] = piece_moved
        self.pieces[piece_moved.color].remove(piece_moved)
        self.grid[start_row][start_col] = None


        #if pieces were jumped, return them to the board
        if jumped_piece:
            row, col = jumped_piece.location
            self.grid[row][col] = jumped_piece
            #if game.jump_bool:
                #game.jump_bool = False


class Piece:
    "Class to represent each piece on the board"

    def __init__(self, color : str, location : tuple, is_king = False, is_captured = False):
        """
        Constructor
        Args:
            color (str): the color of the piece
            location (tuple): coordinate location of the piece on the board
            is_king (bool, optional): whether the piece is a king or not.
            Defaults to False.
            is_captured (bool, optional): whether the piece has been captured
        Raises:
            ValueError: if location does not exist on the board
        """

        self.color = color
        self.location = location
        self.is_king = is_king
        self.became_king = False

    def make_king(self):
        """
        Method to make a piece a king
        """
        self.is_king = True


class Game:
    "Class to represent the game being played"

    def __init__(self, board : Board, end_game = False):
        """
        Constructor
        Args:
            board (Board): the board containing the current game
            current_player (str): the player whose turn it is
            end_game (bool): whether the game is over or not
        Raises:
            ValueError: if the current player name does not exist
        """
        self.draw_offered = False
        self.board = board
        self.current_player = "B" #Player with black pieces plays first
        self.jump_bool = False
        self.end_game = end_game
        self.winner = None
        self.players = {1: "R",
                        2: "B"}
        self.score = [0,0]

        self._alternate_colors()
    #
    # PUBLIC METHODS
    #


    def resign(self, player : str) -> None:
        """
        Allows a player to resign from the game, thereby ending it.
        Args:
            player(str): the player that would like to resign
        Returns:
            None
        """

        if self.players[1] == self.current_player:
            self.score[1] += 1
        else:
            self.score[0] += 1
        self.end_game = True
        self.board.teminal_board = True
        self.winner = 'B' if self.current_player == 'R' else 'R'

    def offer_draw(self) -> None:
        """
        Allows a player to offer a draw, thereby ending the game.
        Args:
            player(str): the player that would like to offer the draw
        Returns:
            None
        """
        self.draw_offered = True

    def accept_reject_draw(self, player : str, accept: bool) -> bool:
        """
        Allows a player to accept another player's draw offer. If the player
        agrees, the end_game attribute will be updated to be True.
        Args:
            player (str): the player that is accepting the draw.
        Returns:
            bool: returns True if player accepts the offer, False otherwise
        """
        if not self.draw_offered:
            return
        if accept:
            self.end_game = True
            self.board.terminal_board = True
            self.winner = None
        else:
            self.draw_offered = False

    def move(self, piece, destination : tuple) -> None:
        """
        Public method for moving pieces on the board. This method checks for
        the validity of the move, whether the piece being moved is already a
        king, and whether the piece being moved should become a king.
        Args:
            piece (piece object): piece to move
            destination (tuple): tuple containing the coordinates of where the
            user would like to move the piece
        Raises:
            ValueError: if the destination is not a valid coordinate pair on the
            board
        Returns:
            None
        """
        # Check if the move is valid
        #print(f"piece all moves is: {self.piece_all_moves(self.board, piece)} for {piece.location}")
        if destination not in self.piece_all_moves(self.board, piece):
            raise ValueError(f"Invalid move, cannot move {piece.location} to {destination}")

        # Update the is_king attribute if the piece becomes a king

        if self.is_valid_move(piece,destination) is False:
            raise ValueError("Inputed move is not valid")
        if self._jumps_available_tf == True and len(self._piece_moves_jumps(self.board, piece)[0] == 0):
            raise ValueError("Move a piece that has jumps available")
        if not self.is_valid_move(piece, destination):
            raise ValueError("Invalid move")
        if not piece.is_king:
            if (piece.color == 'R' and destination[0] == self.board.size - 1) or \
                    (piece.color == 'B' and destination[0] == 0):
                piece.make_king()
                if piece.color == "R":
                    self.board.red_kings += 1
                else:
                    self.board.black_kings += 1

        # Move the piece to the new location
        self.board.remove_piece(piece)
        jumped_piece = self.board.get_piece_between(piece.location, destination)
        if jumped_piece:
            self.board.remove_piece(jumped_piece)
        piece.location = destination
        self.board.add_piece(piece)
        piece.location = destination
        # swap turns
        # This is the first part of my janky way to implement double jumps
        # Feel free to change it I just want it to be testable for the tui
        # If the conditional is present the game will not switch turns until
        # a second move is made or passed on.
        if not jumped_piece or len(self.piece_all_jumps(piece)) == 0:
            self._alternate_turns()
        #self._alternate_turns()
        winner = self.winner_loser(self.board)
        if winner is not None:
            self.winner = winner
            if self.players[1] == winner:
                self.score[0] += 1
            else:
                self.score[1] += 1
            self.end_game = True
            self.board.teminal_board = True

    def is_valid_move(self, piece : Piece, destination : tuple) -> bool:
        """
        Checks if a move is valid.
        Args:
            piece (Piece): the piece that is to be moved
            destination (tuple): tuple containing the coordinates of where the
            user would like to move the piece
        Raises:
            ValueError: if destination is not a valid coordinate pair on the
            board
        Returns:
            bool: True if the move is valid, False otherwise.
        """
        if piece.color != self.current_player:
            return False
        if destination not in self.piece_all_moves(self.board, piece):
            return False
        return True

    def jump(self, piece_to_jump, destination) -> None:
        """
        Method for "jumping" over another piece. If this results in knighting
        or capture, the appropriate attributes of the "jumped" piece will be
        updated.
        Args:
            piece_to_jump (Piece): the piece that is to be jumped
            destination (tuple): the location that the piece will land after
            jumping
        Raises:
            ValueError: if destination is not a valid coordinate pair on the
            board
        Returns:
            None
        """

        raise NotImplementedError #I think this should be included in move

    def piece_all_jumps(self, piece: Piece) -> list:
        """
        Takes a board and a specific piece on the board and returns a list
        of all the available jumps for that piece.
        Args:
            board (Board): the board containing the current game
            piece (Piece): the piece for which all available moves will be
            given
        Returns:
            list[tuples]: list of all available jumps this piece can make
        """
        return self._piece_moves_jumps(self.board, piece)[0]

    def piece_all_moves(self, board : Board, piece : Piece) -> list:
        """
        Takes a board and a specific piece on the board and returns a list
        of all the available moves for that piece.
        Args:
            board (Board): the board containing the current game
            piece (Piece): the piece for which all available moves will be
            given
        Returns:
            list[tuples]: list of all available moves this piece can make
        """
        jumps = self._piece_moves_jumps(board, piece)[0]
        moves = self._piece_moves_jumps(board, piece)[1]
        if jumps:
            return jumps
        elif self.jump_bool == False:
            return moves
        else:
            return

    def player_all_moves(self, board : Board, color: str) -> list:
        """
        Given a board, returns all the moves for the player whose turn it is
        (player 1 or player 2).
        Args:
            board (Board): the board containing the current game
        Returns:
            list: lists of the players player's moves as a tuple of location and
            destination
        """
        moves = {"moves":[], "jumps":[]}
        #for col in board.pieces.values():
        for piece in board.pieces[color]:
            piece_jumps = self._piece_moves_jumps(board,piece)[0]
            piece_moves = self._piece_moves_jumps(board,piece)[1]
            if piece_jumps:
                moves["jumps"].extend([(piece.location, move, piece) for move in piece_jumps])
                self.jump_bool = True
                continue
            elif self.jump_bool == False:
                moves["moves"].extend([(piece.location, move, piece) for move in piece_moves])
            else:
                continue

        if len(moves["jumps"]) > 0:
            return moves["jumps"]
        return moves["moves"]

    def winner_loser(self, board : Board) -> str or None:
        """
        Checks if there is a winner and returns the winning player. If there is
        no winner or if the players agree to a draw, returns None.
        Args:
            board (Board): board containing the current game
        Returns:
            str | None: the name of the player who has won
        """
        all_moves = self.player_all_moves(board, self.current_player)
        if len(board.get_all_pieces("B")) == 0:
            #if all black pieces have been captured, red wins
            print("all the black pieces have been captured")
            return "R"
        elif len(board.get_all_pieces("R")) == 0:
            #if all red pieces have been captured, black wins
            print("all the red pieces have been captured")
            return "B"
        elif not all_moves:
            #there are no legal moves for the current player
            print("there are no legal moves for the current player")
            if self.current_player == "B":
                print(f"all moves for B are: {all_moves}")
                return "R"
            else:
                print(f"all moves for R are: {all_moves}")
                return "B"
        else:
            #there is no winner
            return None

    def rematch(self) -> None:
        """
        Method that resets the game's board, winner, and end_game state to for
        a rematch. Also alternates players' piece colors.
        """
        self.board.reset_board()
        self.winner = None
        self.end_game = False
        self.board.terminal_board = False
        self.draw_offered = False
        self._alternate_colors()
        self.current_player = "B"

    #
    # PRIVATE METHODS
    #

    def _jumps_available_tf(self, board):
        for col in board.pieces.values():
            for piece in col:
                if piece.color == self.current_player:
                    if len(self._piece_moves_jumps(board, piece)[0]) > 0:
                        self.jump_bool = True
        return self.jump_bool

    def _alternate_colors(self) -> None:
        """
        Private method that alternates the players' colors between each game.
        """
        c1 = self.players[1]
        c2 = self.players[2]
        self.players[1] = c2
        self.players[2] = c1

    def _alternate_turns(self) -> None:
        """
        Private method that alternates whose turn it is to play.
        """
        self.jump_bool = False
        if self.current_player == "R":
            self.current_player = "B"
        else:
            self.current_player = "R"


    def _piece_moves_jumps(self, board: Board, piece: Piece) -> list:
        """
        Private method that takes a board and a specific piece on the board
        and returns a tuple containing a list of all the available jumps and
        a list of of all the available moves for that piece.
        Args:
            board (Board): the board containing the current game
            piece (Piece): the piece for which all available moves will be
            given
        Returns:
            tuple[list[tuples]]: tuple of list of all available moves
        """
        moves = []
        jumps = []

        row, col = piece.location

        if piece.is_king:
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        elif piece.color == 'B':
            directions = [(-1, 1), (-1, -1)]
        else:
            directions = [(1, 1), (1, -1)]

        for direction in directions:
            d_row, d_col = direction
            next_row, next_col = row + d_row, col + d_col

            if not (0 <= next_row < board.size and 0 <= next_col < board.size):
                continue

            next_square = board.grid[next_row][next_col]

            if next_square is None:
                moves.append((next_row, next_col))
            elif next_square.color != piece.color:
                jump_row, jump_col = next_row + d_row, next_col + d_col

                if not (0 <= jump_row < board.size and
                    0 <= jump_col < board.size):
                    continue

                jump_square = board.grid[jump_row][jump_col]

                if jump_square is None:
                    jumps.append((jump_row, jump_col))

        return (jumps, moves)
