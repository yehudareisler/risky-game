import random
from card import Card, CardType


class Game:
    game_board = None
    game_state = None
    players = []
    game_pile = []

    def __init__(self, game_board, game_state, players, game_pile):
        self.game_board = game_board
        self.game_state = game_state
        self.players = players
        self.game_pile = game_pile

    @staticmethod
    def get_initial_army_count(player_count):
        return 50 - 5 * player_count

    @staticmethod
    def dice_roll():
        return random.randint(1, 6)

    def execute_setup(self):
        # decide initial army count based on the number of players
        initial_army_count = Game.get_initial_army_count(len(self.players))
        for player in self.players:
            player.available_troops = initial_army_count

        # decide the first player to move based on dice roll
        maxi = 0
        maxi_player = -1
        for i in range(self.players):
            dice_roll = Game.dice_roll()
            if dice_roll > maxi:
                maxi = dice_roll
                maxi_player = i

        # reorder players based on the first to move
        Game.reorder_players_by_next_to_move(self, maxi_player)

        # claim the territories
        unclaimed_territories = self.game_board.territories
        while len(unclaimed_territories) > 0:
            for i in range(self.players):
                if self.players[i].available_troops > 0:
                    claimed_territory_name = self.players[i].claim_territory(self.game_state)
                    self.players[i].available_troops -= 1
                    del unclaimed_territories[claimed_territory_name]
                    if len(unclaimed_territories) == 0:
                        next_to_move = Game.get_next_player_index(self, i)
                        Game.reorder_players_by_next_to_move(self, next_to_move)
                        break

        # add troops to claimed territories
        while Game.players_have_available_troops(self):
            for i in range(self.players):
                if self.players[i].available_troops > 0:
                    self.players[i].reinforce_territory(self.game_state)

        # shuffle card pile
        self.game_pile.shuffle()

        # reorder players on the first to move
        Game.reorder_players_by_next_to_move(self, maxi_player)

    def play_game(self):
        pass

    def reorder_players_by_next_to_move(self, next_player_index):
        self.players = self.players[next_player_index:] + self.players[:next_player_index]

    def get_next_player_index(self, current_player_index):
        if current_player_index + 1 == len(self.players):
            return 0
        else:
            return current_player_index + 1

    def players_have_available_troops(self):
        result = False
        for player in self.players:
            if player.available_troops > 0:
                result = True
                break

        return result
