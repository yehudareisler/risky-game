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
from planner_agent import PlannerAgent
from plan_committer import PlanCommitter
from greedy_agent import GreedyAgent

passive_bt = ("passive", PassiveAgent)
random_bt = ("random", RandomAgent)
attack_above_three_bt = ("attack_above_three", AttackAboveThreeAgent)
reinforce_continent_bt = ("continent_reinforcer", ReinforceContinentAttackAgent)
committing_reinforce_continent_bt = ("committer", CommittingReinforceContinentAgent)
ratio_bt = ("ratio", RatioAgent)
planner_bt = ("planner", PlannerAgent, (100, PlanCommitter))
greedy_bt = ("greedy", GreedyAgent)

players = [passive_bt, random_bt, attack_above_three_bt, reinforce_continent_bt,
           committing_reinforce_continent_bt, ratio_bt, planner_bt]


def main(bot_1, bot_2):
    board = Board.from_config_file('board.cfg')
    pile = Pile.from_config_file('pile.cfg')

    players = [
        Player(bot_1[0], bot_1[1]() if len(bot_1) == 2 else bot_1[1](*bot_1[2])),
        Player(bot_2[0], bot_2[1]() if len(bot_2) == 2 else bot_2[1](*bot_2[2]))
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
        Player(bot_1[0], bot_1[1]() if len(bot_1) == 2 else bot_1[1](*bot_1[2])),
        Player(bot_2[0], bot_2[1]() if len(bot_2) == 2 else bot_2[1](*bot_2[2]))
    ]
    game_count = iterations
    player1_winner_count = 0
    total_move_count = 0

    for i in range(game_count):
        new_board = copy.deepcopy(board)
        new_pile = copy.deepcopy(pile)
        new_players = copy.deepcopy(players)
        player1 = new_players[0]
        state = State(new_board, new_players, new_pile, verbose=False, display_plot=False)
        game = Game(state, with_neutrals=False)
        game.execute_setup()
        game.play_game()
        # if i % 5 == 0:
        #     print(f'At game #{i:04}')
        # print(f'At game #{i:04}')
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
            Player(bot_1[0], bot_1[1]() if len(bot_1) == 2 else bot_1[1](*bot_1[2])),
            Player(bot_2[0], bot_2[1]() if len(bot_2) == 2 else bot_2[1](*bot_2[2]))
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
            # if i % 100 == 0:
            print(f'At game #{i:04}')
            total_move_count += game.move_count
            if player_1 == game.winner:
                bot1_win_count += 1

        print(f'Percentage of games won by {bot_1[0]}: '
              f'{round(bot1_win_count / game_count * 100, 2)}%')
        print(f'Percentage of games won by {bot_2[0]}: '
              f'{round(100 - (bot1_win_count / game_count * 100), 2)}%')
        print(f'Average number of total moves in a game: {round(total_move_count / game_count, 2)}')


def get_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def get_valid_input(prompt, possibilities, is_int=False):
    res = input(prompt)
    res = int(res) if (is_int and get_int(res)) else res
    while res not in possibilities:
        if res == "exit":
            exit()
        res = input("That was not a valid possibility. Please enter a valid possibility, "
                    "according to the following instructions or 'exit' to exit.\n" + prompt)
        res = int(res) if (is_int and get_int(res)) else res
    return res


def print_players():
    print("The possible players are numbered as follows:")
    for n, player in enumerate(players):
        print(n, player[0])


def decide_action():
    choice = get_valid_input(
        "Would you like to run a single game with an interface, or measure the results "
        "of many games?\nWrite 'interface' for the former possibility, and 'measure' "
        "for the latter.\n", possibilities=['interface', 'measure'])
    if choice == 'interface':
        print("We will run a game with an interface.")
        print_players()
        first = get_valid_input("enter the number of the first bot.\n", range(len(players)),
                                is_int=True)
        second = get_valid_input("enter the number of the second bot.\n", range(len(players)),
                                 is_int=True)
        first_player = players[first]
        second_player = players[second]
        main(first_player, second_player)
    elif choice == 'measure':
        repetitions = get_valid_input("We will run a set of games and measure the performance of "
                                      "each bot.\nHow many games should be played?\n",
                                      range(10 ** 6), is_int=True)
        print_players()
        first = get_valid_input("enter the number of the first bot.\n", range(len(players)),
                                is_int=True)
        second = get_valid_input("enter the number of the second bot.\n", range(len(players)),
                                 is_int=True)
        first_player = players[first]
        second_player = players[second]
        test2bots(first_player, second_player, repetitions)


"""
Would you like to run a single game with an interface, or measure the results of many 
games?
Write 'interface' for the former possibility, and 'measure' for the latter.

We will run a game with an interface.
The possible players are numbered as follows:
...
enter the number of the first bot.

enter the number of the second bot.
<RUN>

We will run a set of games and measure the performance of each bot.
How many games should be played?

The possible players are numbered as follows:
...
enter the number of the first bot.

enter the number of the second bot.
<RUN>

That was not a valid possibility. Please enter a valid possibility, according to the 
following 
instructions or 'exit' to exit.
"""


def old_client_interface():
    if len(argv) != 2:
        print("ERR: wrong number of arguments. Enter exactly one argument - main or test")
    if argv[1] == "main":
        main(greedy_bt, committing_reinforce_continent_bt)
    elif argv[1] == "test":
        test()
    elif argv[1] == "test2bots":
        test2bots(committing_reinforce_continent_bt, planner_bt, iterations=50)
    elif argv[1] == "testbots":
        testbots([greedy_bt, attack_above_three_bt, random_bt, reinforce_continent_bt,
                  committing_reinforce_continent_bt, ratio_bt], iterations=30)
    elif argv[1] == "testplanner":
        for i in range(10, 200, 5):
            print(f"testing with {i} branches:")
            new_planner_bt = ("planner", PlannerAgent, (i, PlanCommitter))
            test2bots(committing_reinforce_continent_bt, planner_bt, iterations=50)
    else:
        print(
            "ERR: bad argument. Enter exactly one argument - 'main' or 'test' or 'test2bots' or "
            "'testbots'")


if __name__ == '__main__':
    decide_action()
