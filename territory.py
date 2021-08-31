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
        self.saved_ruler = None
        self.saved_troops = 0
        self.saved_fill_color = ''
        self.is_simulated = False


    def __str__(self):
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

    def can_be_fortify_target(self):
        return self.friendly_fortifiers() and self.enemy_neighbors()

    def start_simulation(self):
        if self.is_simulated:
            raise Exception("cannot simulate over a simulation")
        self.saved_ruler = self.ruler
        self.saved_troops = self.troops
        self.saved_fill_color = self.fill_color
        self.is_simulated = True

    def end_simulation(self):
        if not self.is_simulated:
            raise Exception("cannot end a simulation that didn't start")
        self.ruler = self.saved_ruler
        self.troops = self.saved_troops
        self.fill_color = self.saved_fill_color
        self.is_simulated = False