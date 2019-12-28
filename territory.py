class Territory:
    name = ''
    neighbors = []
    ruler = ''
    troops = 0
    board_pos = ''
    size_on_board = 0
    fill_color = ''
    border_color = ''

    def __init__(self, name, board_pos, size_on_board, border_color):
        self.name = name
        self.board_pos = board_pos
        self.size_on_board = size_on_board
        self.border_color = border_color

    def __repr__(self):
        return self.name

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def is_neutral(self):
        return not self.ruler
