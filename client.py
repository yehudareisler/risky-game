import copy
import itertools
from sys import argv

from game import Game
from board import Board

from pile import Pile
from player import Player
from state import State

# from human_agent import HumanAgent
from random_agent import RandomAgent
from passive_agent import PassiveAgent
from attack_above_three_agent import AttackAboveThreeAgent
from reinforce_continent_agent import ReinforceContinentAttackAgent
from committing_reinforce_continent_agent import CommittingReinforceContinentAgent
from continent_by_ratio_agent import RatioAgent

passive_bt = ("passive", PassiveAgent)
random_bt = ("random", RandomAgent)
attack_above_three_bt = ("attck_above_three", AttackAboveThreeAgent)
reinforce_continent_bt = ("continent_reinforcer", ReinforceContinentAttackAgent)
committing_reinforce_continent_bt = ("committer", CommittingReinforceContinentAgent)
ratio_bt = ("ratio", RatioAgent)


def main(bot_1, bot_2):
    board = Board.from_config_file('board.cfg')
    pile = Pile.from_config_file('pile.cfg')

    players = [
        Player(bot_1[0], bot_1[1]()),
        Player(bot_2[0], bot_2[1]())
    ]
    state = State(board, players, pile, True, True)
    game = Game(state, with_neutrals=False)
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


def test2bots(bot_1, bot_2, iterations):
    board = Board.from_config_file('board.cfg')
    pile = Pile.from_config_file('pile.cfg')
    players = [
        Player(bot_1[0], bot_1[1]()),
        Player(bot_2[0], bot_2[1]())
    ]
    game_count = iterations
    player1_winner_count = 0
    total_move_count = 0

    for i in range(game_count):
        new_board = copy.deepcopy(board)
        new_pile = copy.deepcopy(pile)
        new_players = copy.deepcopy(players)
        player1 = new_players[0]
        state = State(new_board, new_players, new_pile, False, False)
        game = Game(state, with_neutrals=False)
        game.execute_setup()
        game.play_game()
        if i % 100 == 0:
            print(f'At game #{i:04}')
        total_move_count += game.move_count
        if player1 == game.winner:
            player1_winner_count += 1

    print(f'Percentage of games won by {bot_1[0]}: '
          f'{round(player1_winner_count / game_count * 100, 2)}%')
    print(f'Percentage of games won by {bot_2[0]}: '
          f'{round(100 - (player1_winner_count / game_count * 100), 2)}%')
    print(f'Average number of total moves in a game: {round(total_move_count / game_count, 2)}')


def testbots(bots, iterations):
    """
    :param bots: a list of ("name", bot) tuples
    run 1000 games between every pair, and print win percentages.
    """
    print("pitting the following agents against each other:", [name for name, _ in bots])
    board = Board.from_config_file('board.cfg')
    pile = Pile.from_config_file('pile.cfg')
    for bot_1, bot_2 in itertools.combinations(bots, 2):
        players = [
            Player(bot_1[0], bot_1[1]()),
            Player(bot_2[0], bot_2[1]())
        ]
        game_count = iterations
        bot1_win_count = 0
        total_move_count = 0

        for i in range(game_count):
            new_board = copy.deepcopy(board)
            new_pile = copy.deepcopy(pile)
            new_players = copy.deepcopy(players)
            player_1 = new_players[0]
            state = State(new_board, new_players, new_pile, verbose=False, display_plot=False)
            game = Game(state, with_neutrals=False)
            game.execute_setup()
            game.play_game()
            if i % 100 == 0:
                print(f'At game #{i:04}')
            total_move_count += game.move_count
            if player_1 == game.winner:
                bot1_win_count += 1

        print(f'Percentage of games won by {bot_1[0]}: '
              f'{round(bot1_win_count / game_count * 100, 2)}%')
        print(f'Percentage of games won by {bot_2[0]}: '
              f'{round(100 - (bot1_win_count / game_count * 100), 2)}%')
        print(f'Average number of total moves in a game: {round(total_move_count / game_count, 2)}')


if __name__ == '__main__':
    if len(argv) != 2:
        print("ERR: wrong number of arguments. Enter exactly one argument - main or test")
    if argv[1] == "main":
        main(ratio_bt,committing_reinforce_continent_bt)
    elif argv[1] == "test":
        test()
    elif argv[1] == "test2bots":
        test2bots(ratio_bt, committing_reinforce_continent_bt, iterations=1000)
    elif argv[1] == "testbots":
        testbots([attack_above_three_bt, random_bt, reinforce_continent_bt,
                  committing_reinforce_continent_bt, ratio_bt], iterations=300)
    else:
        print("ERR: bad argument. Enter exactly one argument - 'main' or 'test'")
