class Territory:

    def __init__(self, name, board_pos, size_on_board, border_color):
        self.name = name
        self.board_pos = board_pos
        self.size_on_board = size_on_board
        self.border_color = border_color
        self.neighbors = []
        self.ruler = None
        self.troops = 0
        self.fill_color = ''

    def __repr__(self):
        return self.name

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def is_neutral(self):
        return not self.ruler

    def is_border_territory(self):
        for neighbor in self.neighbors:
            if neighbor.ruler != self.ruler:
                return True

        return False

    def enemy_neighbors(self):
        enemy_neighbors = []
        for neighbor in self.neighbors:
            if neighbor.ruler != self.ruler:
                enemy_neighbors.append(neighbor)

        return enemy_neighbors

    def friendly_neighbors(self):
        friendly_neighbors = []
        for neighbor in self.neighbors:
            if neighbor.ruler == self.ruler:
                friendly_neighbors.append(neighbor)

        return friendly_neighbors

    def friendly_fortifiers(self):
        friendly_fortifiers = []
        for neighbor in self.neighbors:
            if neighbor.troops > 1 and neighbor.ruler == self.ruler:
                friendly_fortifiers.append(neighbor)

        return friendly_fortifiers

    def can_be_attack_source(self, player):
        for neighbor in self.neighbors:
            if neighbor.ruler != player and self.troops > 1:
                return True

        return False

    def can_be_fortify_source(self):
        return self.troops > 1 and self.friendly_neighbors()

    def can_be_fortify_target(self):
        return self.friendly_fortifiers() and self.enemy_neighbors()

