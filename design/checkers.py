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
    
    def __init__(self, length, width) -> None:
        """
        Constructor

        Args:
            length (int): the length of the board
            width (int): the width of the board
        """

        self.pieces = {'player 1': [], 'player 2':[]}

        # list[list[Piece]]: the board
        self._board = [[None] * width for _ in range(length)]

        #int : the number of rows in the board
        self._length = length

        #int : the number of tiles per row
        self._width = width

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
        self.is_captured = is_captured

class Game:
    "Class to represent the game being played"

    def __init__(self, board : Board, current_player : str, end_game = False):
        """
        Constructor

        Args:
            board (Board): the board containing the current game
            current_player (str): the player whose turn it is
            end_game (bool): whether the game is over or not

        Raises:
            ValueError: if the current player name does not exist
        """

        self.board = board
        self.current_player = current_player
        self.end_game = end_game

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
        raise NotImplementedError

    def offer_draw(self, player : str) -> None:
        """
        Allows a player to offer a draw, thereby ending the game.

        Args:
            player(str): the player that would like to offer the draw

        Returns:
            None
        """
        raise NotImplementedError

    def accept_reject_draw(self, player : str) -> bool:
        """
        Allows a player to accept another player's draw offer. If the player
        agrees, the end_game attribute will be updated to be True.

        Args:
            player (str): the player that is accepting the draw.

        Returns:
            bool: returns True if player accepts the offer, False otherwise
        """
        raise NotImplementedError


    def move(self, destination : tuple) -> None:
        """
        Public method for moving pieces on the board. This method checks for
        the validity of the move, whether the piece being moved is already a
        king, and whether the piece being moved should become a king.

        Args:
            destination (tuple): tuple containing the coordinates of where the
            user would like to move the piece

        Raises:
            ValueError: if the destination is not a valid coordinate pair on the
            board

        Returns:
            None
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def jump(self, piece_to_jump, destination) -> None:
        """
        Method for "jumping" over another piece. If this results in knighting or
        capture, the appropriate attributes of the "jumped" piece will be
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

        raise NotImplementedError

    def piece_all_moves(self, board : Board, piece : Piece) -> list:
        """
        Takes a board and a specific piece on the board and returns a list
        of all the available moves for that piece.

        Args:
            board (Board): the board containing the current game
            piece (Piece): the piece for which all available moves will be given

        Returns:
            list: list of all available moves this piece can make
        """
        raise NotImplementedError

    def player_all_moves(self, player : str, board : Board) -> dict:
        """
        Given a board, returns all the moves for the specificed player
        (player 1 or player 2).

        Args:
            board (Board): the board containing the current game

        Returns:
            dict: dictionary of each player's piece as keys mapped to a list of
            all its possible moves
        """
        raise NotImplementedError

    def winner_loser(self, board : Board) -> str or None:
        """
        Checks if there is a winner and returns the winning player. If there is
        no winner or if the players agree to a draw, returns None.

        Args:
            board (Board): board containing the current game

        Returns:
            str | None: the name of the player who has won
        """
        raise NotImplementedError

    #
    # PRIVATE METHODS
    #

    def _alternate_colors(self) -> None:
        """
        Private method that alternates the players' colors between each game.
        """
        raise NotImplementedError


    def _alternate_turns(self) -> None:
        """
        Private method that alternates whose turn it is to play.
        """
        raise NotImplementedError
