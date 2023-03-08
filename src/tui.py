import time
import click
from colorama import Fore, Style
from checkers import Piece, Board, Game
from bots import RandomBot, SmartBot

class TUIPlayer:
    """
    Class for each player using the tui.
    Attributes:
        color(str): the color of the player's pieces
        n(int): The number of the player
        type(str): Whether the player is a human, a random bot, or a smart bot
        board(Board): The board that the player is playing on
        game(Game): The game that the player is playing with
    """
    def __init__(self, board: Board, n: int, player_type: str,
        game: Game, delay = 0.5):
        self.color = game.players[n]
        if player_type == "human":
            self.name = f"Player {n}"
            self.bot = None
        elif player_type == "random":
            self.name = f"random bot {n}"
            self.bot = RandomBot(game, self.color)
        else:
            self.name  = f"smart bot {n}"
            self.bot = SmartBot(game, self.color)
        self.n = n
        self.type = player_type
        self.board = board
        self.game = game
        self.draw_count = 0
        self.delay = delay

    def check_if_valid(self,loc: list) -> bool:
        """
        Helper method that checks if the square selected is a valid tile.
        If the square is not on the board or the square is not two intigers
        divided by a comma the method returns false.
        """
        if len(loc) != 2:
            print_board(self.board)
            print("Please enter move in valid format. \n")
            return False
        try:
            int(loc[0]), int(loc[1])
        except:
            print_board(self.board)
            print("Please enter move in valid format. \n")
            return False
        return True

    def proccess_selection(self, input: str) -> Piece:
        """
        Method that processes a move input and returns either a processed
        location or None if the move is not valid
        """
        if input == "I resign":
            self.game.resign(self.n)
            return "break"
        elif input == "draw":
            if self.draw_count > 0:
                self.draw_count += 1
            else:
                self.game.offer_draw()
                print("draw offered")
                self.draw_count += 1
                self.game._alternate_turns()
                return "break"
        loc = input.split(",")
        if self.check_if_valid(loc) is False:
            return "continue"
        loc[0] = int(loc[0]) - 1
        loc[1] = int(loc[1]) - 1
        if type(self.board.grid[loc[0]][loc[1]]) is Piece:
            p = self.board.grid[loc[0]][loc[1]]
        else:
            print_board(self.board)
            print("Please select a square containing a piece")
            return "continue"
        if p.color != self.color:
            print_board(self.board)
            print("You can only move your own pieces")
            return "continue"
        return p

    def get_jump(self, piece: Piece) -> None:
        """
        Method that asks the player to input a jump if they are able to make a
        second jump.
        """
        all = self.game.piece_all_jumps(piece)
        filtered_all = [tuple([x + 1 for x in tup]) for tup in all]
        print_board(self.board, piece, all)
        if self.type == "human":
            print("You may now do extra jumps")
            print(f"Possible jumps are {filtered_all}")
            while self.color == self.game.current_player:
                destination = input("Please enter your intended jump location")
                dest = destination.split(",")
                if self.check_if_valid(dest) is False:
                    continue
                dest[0] = int(dest[0]) - 1
                dest[1] = int(dest[1]) - 1
                if tuple(dest) not in all:
                    print_board(self.board)
                    print("Please enter move in valid format.")
                    continue
                self.game.move(piece, tuple(dest))
        else:
            while self.color == self.game.current_player:
                destination = self.bot.suggest_move()
                if destination[0] == piece:
                    self.game.move(piece, destination[1])

    def get_move(self) -> None:
        """
        Method that asks the player to input a move and makes the move
        if it is valid.
        """
        self.color = self.game.players[self.n]
        if self.type == "human":
            while self.color == self.game.current_player:
                # Prints board and explains possible inputs
                if self.game.draw_offered is True:
                    while self.game.draw_offered is True:
                        print("Your opponent has offered a draw")
                        offer = input("Do you accept? (Yes/No) \n")
                        if offer != "Yes" and offer != "No":
                            continue
                        accept = (offer == "Yes")
                        self.game.accept_reject_draw(self.n, accept)
                        break
                    self.game._alternate_turns()
                    break
                print("piece must be chosen in the format 'row,column'")
                if self.draw_count > 1:
                    print("Please do not spam draw offers")
                else:
                    print("Resign by entering 'I resign' offer a draw w/'draw'")
                # Requests move
                selected =input(f"What piece would {self.name} like to move?\n")
                # Processes move
                piece = self.proccess_selection(selected)
                if piece == "continue":
                    continue
                elif piece == "break":
                    break
                # requests destination
                all = self.game.piece_all_moves(self.board, piece)
                if all:
                    filtered_all = [tuple([x + 1 for x in tup]) for tup in all]
                else:
                    print_board(self.board)
                    print("No legal moves for this piece")
                    print("If you can jump over a piece you must")
                    continue
                print_board(self.board, piece.location, all)
                print(filtered_all)
                print("to select a different piece enter a blank line")
                destination=input(f"Where would {self.name} like to move it?\n")
                # Processes destination
                dest = destination.split(",")
                if self.check_if_valid(dest) is False:
                    continue
                dest[0] = int(dest[0]) - 1
                dest[1] = int(dest[1]) - 1
                self.draw_count = 0
                try:
                    self.game.move(piece, tuple(dest))
                except ValueError:
                    print("Please enter valid move")
                    continue
                if self.color == self.game.current_player:
                    self.get_jump(piece)
        else:
            # Do bot things need to see bot implimentation
            # Ask for a column (and re-ask if
            # a valid column is not provided)
            self.bot._color = self.color
            while self.color == self.game.current_player:
                if self.game.draw_offered is True:
                    self.game.accept_reject_draw(self.n, False)
                move = self.bot.suggest_move()
                time.sleep(self.delay)
                print(f"{self.name} moves {move[0].location, move[1]}")
                self.game.move(move[0], move[1])
                if self.game.current_player == self.color:
                    self.get_jump(move[0])

    def play_again(self) -> bool:
        """
        Method that asks a player if they would like to play another round.
        """
        again = input("Would you like to play again (Yes/No) \n")
        if again == "Yes":
            return True
        return False

    def __str__(self):
        return self.name

color_dict = {"R": Fore.RED, "B": Fore.BLACK}


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

def play_checkers(game: Game, board: Board, players) -> None:
    """
    Function that plays a game of checkers between two TUIplayers.
    """

    turn_count = 0
    while game.end_game is False:
        print_board(board)
        print()
        if game.players[1] == game.current_player:
            num = 1
        else:
            num = 2
        players[num].get_move()
        turn_count += 0.5
    print()
    print_board(board)
    if game.winner is not None:
        if game.players[1] == game.winner:
            print(f"{players[1]} Wins!")
        else:
            print(f"{players[2]} Wins!")
    else:
        print("It's a draw!")
    print(f"The game took {turn_count} turns.")

def ask_for_rematch(game: Game, players) -> None:
    """
    Function that asks both players if they want a rematch. Bots always
    agree to rematches if playing against a human. Otherwise both players
    must accept the rematch proposal. If either player says no the game ends.
    """

    print(f"the score is {game.score[0]} to {game.score[1]}")
    if players[2].bot and players[1].play_again():
        return True
    elif players[1].bot and players[2].play_again():
        return True
    elif not players[1].bot and not players[2].bot:
        if players[1].play_again() and players[2].play_again():
            return True
    return False

@click.command()

@click.option("--player1", prompt="player1 type",type=click.Choice([
            'human', 'random','smart'], case_sensitive=False),
            default="human", help="human, random bot or smart bot")
@click.option("--player2", prompt="player2 type",type=click.Choice([
            'human', 'random','smart'], case_sensitive=False),
            default = "random", help="human, random bot or smart bot")
@click.option("--bot_delay", prompt = "bot delay", default=0.5,
            help="Delay between bot moves")
@click.option("--size", prompt="board size", default=8, help="board size")
@click.option("--rounds", prompt="how many rounds would you like to play?",
            default=1)
def cmd(player1: str, player2: str, bot_delay: int, size: int, rounds: int
        ) -> None:

    if len(str(size)) != 1 and len(str(size)) != 2:
        print("Please enter size as an int between 6 and 20.")
        return
    try:
        size = int(size)
    except:
        print("Please enter size as an int between 6 and 20.")
        return
    if size > 20 or size < 6:
        print("Please enter a size between 6 and 20")
        return
    print()
    board = Board(size)
    game = Game(board)
    p1 = TUIPlayer(board, 1, player1, game, bot_delay)
    p2 = TUIPlayer(board, 2, player2, game, bot_delay)

    players = {1: p1, 2: p2}
    while True:
        rounds -= 1
        play_checkers(game, board, players)
        print(f"There are {rounds} rounds remaining")
        game.rematch()
        if rounds < 1:
            if ask_for_rematch(game, players) is False:
                break
    print(f"The final score is {game.score[0]} to {game.score[1]}")

if __name__ == "__main__":
    cmd()