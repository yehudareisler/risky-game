import copy
from sys import argv

from game import Game
from board import Board
from human_agent import HumanAgent
from pile import Pile
from player import Player
from random_agent import RandomAgent
from passive_agent import PassiveAgent
from state import State


def main():
    board = Board.from_config_file('board.cfg')
    pile = Pile.from_config_file('pile.cfg')
    players = [
        Player('Random', PassiveAgent()),
        Player('Passive', PassiveAgent())
    ]
    state = State(board, players, pile, True, True)
    game = Game(state)
    game.execute_setup()
    game.play_game()
    board.plotly_display.disp()


def test():
    board = Board.from_config_file('board.cfg')
    pile = Pile.from_config_file('pile.cfg')
    players = [
        Player('Bot_1', RandomAgent()),
        Player('Bot_2', RandomAgent())
    ]
    game_count = 10000
    starter_winner_count = 0
    total_move_count = 0

    for i in range(game_count):
        new_board = copy.deepcopy(board)
        new_pile = copy.deepcopy(pile)
        new_players = copy.deepcopy(players)
        state = State(new_board, new_players, new_pile, False, False)
        game = Game(state)
        game.execute_setup()
        game.play_game()
        print(f'At game #{i:04}')
        total_move_count += game.move_count
        if game.starter == game.winner:
            starter_winner_count += 1

    print(f'Percentage of games won by starter: {starter_winner_count / game_count * 100}%')
    print(f'Average number of total moves in a game: {total_move_count / game_count}')


if __name__ == '__main__':
    if len(argv) != 2:
        print("ERR: wrong number of arguments. Enter exactly one argument - main or test")
    if argv[1] == "main":
        main()
    elif argv[1] == "test":
        test()
    else:
        print("ERR: bad argument. Enter exactly one argument - 'main' or 'test'")
