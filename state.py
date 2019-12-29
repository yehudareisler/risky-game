class State:

    def __init__(self, board, players, pile, verbose, display_plot):
        self.board = board
        self.players = players
        self.card_set_count = 0
        self.verbose = verbose
        self.display_plot = display_plot
        self.player_to_move = None
        self.player_to_wait = None
        self.pile = pile
        self.attack_successful = False

    def get_card_bonus(self):
        if self.card_set_count < 6:
            return 2 + self.card_set_count*2
        else:
            return 15 + (self.card_set_count - 6)*5
