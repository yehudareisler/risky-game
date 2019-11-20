from continent import Continent
from territory import Territory
from path import Path


class GameMap:
    # territories = {}
    # paths = {}
    game_map = {}
    game_map.continents = {}
    game_map.territories = []
    game_map.paths = []
    # continents = {}

    def __init__(self, territories, paths):
        self.territories = territories
        self.paths = paths

    def initialize_from_config_file(self, path_to_file):
        with open(path_to_file) as f:
            continent_count, territory_count = map(int, f.readline().split())

            # read continents and their respective territories
            for _ in range(continent_count):
                continent_name = f.readline()
                continent_bonus, continent_territory_count = map(int, f.readline().split())
                self.game_map.continents[continent_name]['armyBonus'] = continent_bonus
                self.game_map.continents[continent_name]['territories'] = []

                for _ in range(continent_territory_count):
                    new_territory_name = f.readline()
                    new_territory = Territory(new_territory_name)
                    self.continents[continent_name]['territories'].append(new_territory_name)
                    self.territories[new_territory_name]

                f.readline()

            # read territories and their neighbors
            for _ in range(territory_count):
