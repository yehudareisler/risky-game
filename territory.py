class Territory:
    name = ''
    neighbors = []
    ruler = ''
    troops = 0
    board_pos = ''
    board_height = 0
    board_width = 0
    fill_color = ''
    border_color = ''

    def __init__(self, name, board_pos, board_height, board_width, border_color):
        self.name = name
        self.board_pos = board_pos
        self.board_height = board_height
        self.board_width = board_width
        self.border_color = border_color

    def __repr__(self):
        return self.name

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def is_neutral(self):
        return not self.ruler
