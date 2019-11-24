class State:
    phase = 0
    game_board = None
    card_set_count = 0

    def __init__(self, phase, game_board):
        self.phase = phase
        self.game_board = game_board
        self.card_set_count = 0

    def get_card_bonus(self):
        if self.card_set_count < 6:
            return 2 + self.card_set_count*2
        else:
            return 15 + (self.card_set_count - 6)*5
