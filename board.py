import networkx as nx
from networkx.drawing.nx_agraph import to_agraph

from continent import Continent
from path import Path
from territory import Territory


class Board:
    territories = {}
    paths = []
    continents = {}

    def __init__(self, territories, paths, continents):
        self.territories = territories
        self.paths = paths
        self.continents = continents

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

    def plot(self):
        G = nx.Graph()
        for territory in self.territories.values():
            label = territory.name + ', t = ' + str(territory.troops)
            G.add_node(territory, label=label, shape='circle')
        print('Nodes: ', G.nodes)
        my_edges = [(path.from_territory, path.to_territory) for path in self.paths]
        G.add_edges_from(my_edges)
        print('Edges: ', G.edges)
        A = to_agraph(G)
        A.graph_attr.update(overlap='false', splines='true')
        A.layout()
        A.draw('test_graph.png', prog='neato')

    @staticmethod
    def from_config_file(path_to_file):
        new_territories = {}
        new_paths = []
        new_continents = {}

        with open(path_to_file) as f:
            continent_count, territory_count = map(int, f.readline().split())

            # read continents and their respective territories
            for _ in range(continent_count):
                continent_name = f.readline().strip()
                continent_bonus, continent_territory_count = map(int, f.readline().split())
                new_continent = Continent(continent_name, [], continent_bonus)
                new_continents[continent_name] = new_continent

                for _ in range(continent_territory_count):
                    new_territory_name = f.readline().strip()
                    new_territory = Territory(new_territory_name)
                    new_continent.add_territory(new_territory)
                    new_territories[new_territory_name] = new_territory

                f.readline()

            # read territories and their neighbors
            for _ in range(territory_count):
                from_territory_name = f.readline().strip()
                from_territory = new_territories[from_territory_name]

                neighbor_count = int(f.readline())
                for _ in range(neighbor_count):
                    to_territory_name = f.readline().strip()
                    to_territory = new_territories[to_territory_name]
                    from_territory.add_neighbor(to_territory)
                    new_path = Path(from_territory, to_territory)
                    new_paths.append(new_path)

                f.readline()
        return Board(new_territories, new_paths, new_continents)

    def all_neighbors_of_territory(self, target_territory):
        neighbors = []
        for path in self.paths:
            if path.from_territory == target_territory:
                neighbors.append(path.to_territory)

        return neighbors

    def friendly_neighbors_of_territory(self, target_territory):
        neighbors = []
        for path in self.paths:
            if path.from_territory == target_territory:
                if path.to_territory.ruler == path.from_territory.ruler:
                    neighbors.append(path.to_territory)

        return neighbors

    def occupied_territories(self, player=None):
        occupied_territories = []
        for territory_name in self.territories:
            territory = self.territories[territory_name]
            if territory.ruler == player.name:
                occupied_territories.append(territory)

        return occupied_territories

    def occupied_continents(self, player=None):
        occupied_continents = []
        for continent_name in self.continents:
            continent = self.continents[continent_name]
            continent_ruler = continent.get_ruler()
            if continent_ruler == player:
                occupied_continents.append(continent)

        return occupied_continents
