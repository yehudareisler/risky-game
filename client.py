from game import Game
from board import Board
from pile import Pile

game_board = Board()
game_board.initialize_game_board_from_config_file('board.cfg')
game_pile = Pile()
game_pile.initialize_game_card_pile_from_config_file('pile.cfg')
print(game_board)
