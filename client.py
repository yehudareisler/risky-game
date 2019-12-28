from game import Game
from board import Board
from human_agent import HumanAgent
from pile import Pile
from player import Player
from random_agent import RandomAgent
from state import State


def main():
    board = Board.from_config_file('board.cfg')
    pile = Pile.from_config_file('pile.cfg')
    players = [
        Player('Bot_1', RandomAgent()),
        Player('Bot_2', RandomAgent())
    ]
    state = State(board, True, True)
    game = Game(state, players, pile)
    game.execute_setup()


if __name__ == '__main__':
    main()
