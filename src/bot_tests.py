from bots import RandomBot, SmartBot
from checkers import Piece, Game, Board

def test_random_1():
    board = Board(8)
    game = Game(board)
    bot = RandomBot(board, "B", game)

    piece,move = bot.suggest_move()
    #print(move)

    assert 0 <= move[0] <= 8 and 0 <= move[1] <= 8

test_random_1()

def smart_test_1():
    board = Board(8)
    game = Game(board)
    bot = SmartBot(board, "B", game)

    new_board = bot.suggest_move()
    game._bot_move(new_board)

    assert board != game.board

smart_test_1()
