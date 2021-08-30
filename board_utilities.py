from territory import Territory
from player import Player
from continent import Continent


class BoardUtils:
    # @staticmethod
    # def get_distance(self, source: Territory, target: Territory):
    #     if source.ruler == target.ruler:
    #         return float("inf")
    @staticmethod
    def get_continent_ratio(source: Continent, player: Player):
        player_units, enemy_units = 0, 0
        for territory in source.territories:
            if territory.ruler == player:
                player_units += territory.troops
            else:
                enemy_units += territory.troops
        # print(player_units,enemy_units)
        ret_val = player_units / enemy_units if enemy_units != 0 else float("inf")
        # print("ratio:", ret_val)
        return ret_val