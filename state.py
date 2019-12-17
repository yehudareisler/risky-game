class State:
    phase = 0
    board = None
    card_set_count = 0
    player_to_move = None

    def __init__(self, phase, board, player_to_move):
        self.phase = phase
        self.board = board
        self.card_set_count = 0
        self.player_to_move = player_to_move

    def get_card_bonus(self):
        if self.card_set_count < 6:
            return 2 + self.card_set_count*2
        else:
            return 15 + (self.card_set_count - 6)*5
