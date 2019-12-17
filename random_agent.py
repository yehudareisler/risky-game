import random
import time

from agent import Agent


class RandomAgent(Agent):
    # overriding abstract method
    def reinforce_territory(self, state):
        current_player = state.player_to_move
        territories = current_player.get_occupied_territories(state)
        territory_name = random.choice(territories)
        return territory_name

    # overriding abstract method
    def defend_territory(self, state, attacked_territory):
        troop_count = 1 + random.randint(0, 1)
        return troop_count

    # overriding abstract method
    def wants_to_attack(self, state):
        return bool(random.getrandbits(1))

    # overriding abstract method
    def wants_to_fortify(self, state):
        return bool(random.getrandbits(1))

    # overriding abstract method
    def fortify_territory(self, state):
        current_player = state.player_to_move
        territories = current_player.get_occupied_territories(state)
        to_territory_name = ''
        from_territory_name = ''
        troop_count = 0

        now = time.time()
        end_time = now + 2
        while time.time() < end_time:
            to_territory_name = random.choice(territories)
            neighbors = state.board.get_friendly_neighbors_of_territory(to_territory_name)
            if neighbors:
                from_territory_name = random.choice(neighbors)
                if from_territory_name.troops > 1:
                    troop_count = random.randint(1, from_territory_name.troops - 1)
                    break
            from_territory_name = ''

        return to_territory_name, from_territory_name, troop_count
