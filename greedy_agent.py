import math
import random

from agent import Agent
from heuristcs import get_continent_ratio, choose_best_path, calculate_path_value, find_territory_ratio

ratio = 1.4
log_base = 3.5

def find_attack_path(state, troops_addition = 0):
    cur_player = state.player_to_move
    territories = state.board.border_territories(cur_player)
    for land in territories:
        land_troops = land.troops + troops_addition
        path = choose_best_path(state, land, math.log(land_troops, log_base), land_troops / ratio, cur_player)

    return path


class GreedyAgent(Agent):


    def reinforce_owned_territory(self, state):
        if len(state.board.border_territories(state.player_to_move)) == 0:
            territories = state.board.occupied_territories(state.player_to_move)
            return territories[0]
        path = find_attack_path(state, state.player_to_move.calculate_troops_addition(state))
        # print("path: "  , path[1])
        if len(path) == 0:
            territories = state.board.occupied_territories(state.player_to_move)
            return territories[0]

        return path[0]
        # territories = state.board.territories()
        # return territories[path[0]]

    # overriding abstract method
    def reinforce_neutral_territory(self, state):
        territories = state.board.neutral_territories()
        territory = random.choice(territories)
        return territory

    # overriding abstract method
    def defend_territory(self, state, attacked_territory):
        troop_count = 1
        if attacked_territory.troops > 1:
            troop_count += 1
        return troop_count

    # overriding abstract method
    def select_attack_source(self, state):
        territories = list(state.board.territories_to_attack_from(state.player_to_move))
        territory = random.choice(territories)
        return territory

    # overriding abstract method
    def select_attack_count(self, state, source):
        return source.troops - 1

    # overriding abstract method
    def wants_to_fortify(self, state):
        return False

    # overriding abstract method
    def select_fortify_source(self, state, target):
        source = random.choice(target.friendly_fortifiers())
        return source

    # overriding abstract method
    def select_fortify_target(self, state):
        territories = list(state.board.territories_to_fortify_to(state.player_to_move))
        target = random.choice(territories)
        return target

    # overriding abstract method
    def select_fortify_count(self, state, source):
        troop_count = source.troops - 1
        return troop_count

    def wants_to_attack(self, state):
        if len(state.board.border_territories(state.player_to_move)) == 0 :
            return False
        for land in state.board.border_territories(state.player_to_move):
            for neighbor in land.neighbors:
                if neighbor.ruler != land.ruler:
                    if find_territory_ratio(land, neighbor) >= ratio:
                        return True
        return False


    def select_attack_target(self, state, source):
        # print(find_attack_path(state)[1])
        try :
            return find_attack_path(state)[1]
        except:
            territories = list(source.enemy_neighbors())
            territory = random.choice(territories)
            return territory
