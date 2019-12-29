import networkx as nx
from networkx.drawing.nx_agraph import to_agraph

from continent import Continent
from path import Path
from territory import Territory


class Board:

    def __init__(self, territories, paths, continents):
        self.territories = territories
        self.paths = paths
        self.continents = continents
        # colors indicating occupation: player0, player1, neutrals (blue, red, gray)
        self.territory_colors = ['#283493', '#932834', '#616161']

    def __str__(self):
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

    def plot(self, plot_file_name, verbose):
        if verbose:
            # init graph
            G = nx.Graph()

            # add nodes
            for territory in self.territories.values():
                label = f'{territory.name}\nt = {territory.troops}\n{territory.ruler}'
                # label = f'{territory.name}\nt = {territory.troops}, ({territory.board_pos})'
                G.add_node(territory, label=label, fontsize=30,
                           pos=territory.board_pos, fixedsize=True,
                           height=territory.size_on_board, width=territory.size_on_board,
                           shape='oval', fontcolor='#FFFFFF', penwidth=35,
                           fillcolor=territory.fill_color, color=territory.border_color,  style='filled')

            # add edges
            for path in self.paths:
                G.add_edge(path.from_territory, path.to_territory, penwidth=5)

            # convert to graphviz agraph
            A = to_agraph(G)
            A.graph_attr.update(splines='true', bgcolor='#BDBDBD')
            A.layout()

            # draw and export
            A.draw(plot_file_name)

    @staticmethod
    def from_config_file(path_to_file):
        new_territories = {}
        new_paths = []
        new_continents = {}
        continent_colors = ['#EF6C00', '#9E9D24', '#689F38', '#00ACC1', '#6D4C41', '#F06292']

        with open(path_to_file) as f:
            continent_count, territory_count = map(int, f.readline().split())

            # read continents and their respective territories
            for i in range(continent_count):
                continent_name = f.readline().strip()
                continent_bonus, continent_territory_count = map(int, f.readline().split())
                new_continent = Continent(continent_name, [], continent_bonus)
                new_continents[continent_name] = new_continent

                for _ in range(continent_territory_count):
                    name = f.readline().strip()
                    board_pos, size_on_board = f.readline().strip().split()
                    new_territory = Territory(name, board_pos, size_on_board, continent_colors[i])
                    new_continent.add_territory(new_territory)
                    new_territories[name] = new_territory

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

    def border_territories(self, reinforcing_player):
        border_territories = []
        occupied_territories = self.occupied_territories(reinforcing_player)
        for territory in occupied_territories:
            if territory.is_border_territory():
                border_territories.append(territory)

        return border_territories

    def occupied_territories(self, player):
        occupied_territories = []
        for territory_name in self.territories:
            territory = self.territories[territory_name]
            if territory.ruler == player:
                occupied_territories.append(territory)

        return occupied_territories

    def neutral_territories(self):
        neutral_territories = []
        for territory_name in self.territories:
            territory = self.territories[territory_name]
            if not territory.ruler:
                neutral_territories.append(territory)

        return neutral_territories

    def occupied_continents(self, player):
        occupied_continents = []
        for continent_name in self.continents:
            continent = self.continents[continent_name]
            continent_ruler = continent.get_ruler()
            if continent_ruler == player:
                occupied_continents.append(continent)

        return occupied_continents

    def territories_to_attack_from(self, attacking_player):
        source_territories = set()
        occupied_territories = self.occupied_territories(attacking_player)
        for territory in occupied_territories:
            if territory.can_be_attack_source(attacking_player):
                source_territories.add(territory)

        return source_territories

    def territories_to_fortify_to(self, fortifying_player):
        source_territories = set()
        occupied_territories = self.occupied_territories(fortifying_player)
        for territory in occupied_territories:
            if territory.can_be_fortify_target():
                source_territories.add(territory)

        return source_territories
