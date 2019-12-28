class State:
    board = None
    card_set_count = 0
    player_to_move = None
    verbose = False
    display_plot = False

    def __init__(self, board, verbose, display_plot):
        self.board = board
        self.card_set_count = 0
        self.verbose = verbose
        self.display_plot = display_plot

    def get_card_bonus(self):
        if self.card_set_count < 6:
            return 2 + self.card_set_count*2
        else:
            return 15 + (self.card_set_count - 6)*5
