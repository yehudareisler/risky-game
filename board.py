from continent import Continent
from territory import Territory
from path import Path


class Board:
    territories = {}
    paths = []
    continents = {}

    def __init__(self):
        self.territories = {}
        self.paths = []

    def initialize_game_board_from_config_file(self, path_to_file):
        with open(path_to_file) as f:
            continent_count, territory_count = map(int, f.readline().split())

            # read continents and their respective territories
            for _ in range(continent_count):
                continent_name = f.readline().strip()
                continent_bonus, continent_territory_count = map(int, f.readline().split())
                new_continent = Continent(continent_name, [], continent_bonus)
                self.continents[continent_name] = new_continent

                for _ in range(continent_territory_count):
                    new_territory_name = f.readline().strip()
                    new_territory = Territory(new_territory_name)
                    new_continent.add_territory(new_territory)
                    self.territories[new_territory_name] = new_territory

                f.readline()

            # read territories and their neighbors
            for _ in range(territory_count):
                from_territory_name = f.readline().strip()
                from_territory = self.territories[from_territory_name]

                neighbor_count = int(f.readline())
                for _ in range(neighbor_count):
                    to_territory_name = f.readline().strip()
                    to_territory = self.territories[to_territory_name]
                    from_territory.add_neighbor(to_territory)
                    new_path = Path(from_territory, to_territory)
                    self.paths.append(new_path)

                f.readline()

    def __repr__(self):
        representation = ''
        representation += f'Game map with {len(self.continents.keys())} continents ' \
                          f'and {len(self.territories.keys())} territories:\n'
        representation += '\nContinents:\n'
        for continent_name in self.continents:
            representation += '* ' + str(self.continents[continent_name]) + '\n'
        representation += '\nTerritories:\n'
        for territory_name in self.territories:
            representation += str(self.territories[territory_name]) + '\n'

        # representation += '\nPaths:\n'
        # for path in self.paths:
        #     representation += str(path) + '\n'

        return representation
