import random
from card import Card, CardType
from logger import Logger


class Game:
    state = None
    players = []
    pile = None

    def __init__(self, state, players, pile):
        self.state = state
        self.players = players
        self.pile = pile

    @staticmethod
    def dice_roll():
        return random.randint(1, 6)

    def execute_setup(self, verbose=True):
        Logger.log("Initializing game...\nStarted setup phase.", verbose)
        # 1) decide the first player to move based on dice roll
        maxi = 0
        maxi_player = -1
        for i in range(2):
            dice_roll = Game.dice_roll()
            Logger.log(f'Player {self.players[i]} rolls a {dice_roll}', verbose)
            if dice_roll > maxi:
                maxi = dice_roll
                maxi_player = i

        # 2) reorder players based on the first to move
        Game.reorder_players_by_next_to_move(self, maxi_player)
        player0 = self.players[0]
        player1 = self.players[1]
        Logger.log(f'Player to start: {player0}', verbose)

        # 3)
        # " Remove the Secret Mission cards and the 2 “wild” cards from the RISK card deck.
        #   Shuffle thoroughly and deal the cards, face down, into 3 equal piles.
        #   Both you and your opponent choose a different pile. The remaining pile is neutral. "
        #
        # 4)
        # " Place one of your Infantry onto each of the 14 territories shown on the RISK cards in your pile.
        #   Your opponent does the same.
        #   Then place one “neutral” Infantry onto each of the remaining 14 “neutral” territories. "
        self.assign_cards(player0, player1, False, True)
        exit(0)

        # 5)
        # " After every territory on the board has been claimed,
        #   you and your opponent take turns placing your remaining armies:
        #   Place 2 Infantry onto any 1 or 2 of the territories you occupy.
        #   Then place 1 “neutral” army onto any “neutral” territory you want,
        #   placing it to block your opponent’s possible advance. "
        # Players have 22 troops remaining each.
        for _ in range(11):
            for i in range(2):
                self.state.player_to_move = self.players[i]
                self.players[i].reinforce_owned_territory(self.state)
                self.players[i].reinforce_owned_territory(self.state)
                self.players[i].reinforce_neutral_territory(self.state)

        # 6)
        # " After all the armies have been placed on the board,
        #   return the two “wild” cards to the RISK card deck,
        #   shuffle the deck and start to play. "
        self.pile.add_card(Card(CardType.WILDCARD, None))
        self.pile.add_card(Card(CardType.WILDCARD, None))
        self.pile.shuffle()
        Logger.log('Shuffling cards\nSetup over.', verbose)

    def assign_cards(self, player0, player1, verbose, plot_verbose):
        self.pile.remove_card_with_index(0)
        self.pile.remove_card_with_index(0)
        # cheating until better implementation
        self.pile.shuffle()
        player0_cards = self.pile[:14]
        player1_cards = self.pile[14:28]
        neutral_cards = self.pile[28:42]
        for card in player0_cards:
            territory = self.state.board.territories[card.territory_name]
            territory.ruler = player0.name
            territory.troops = 1
            Logger.log(f'Territory {territory} taken by {player0}', verbose)
        for card in player1_cards:
            territory = self.state.board.territories[card.territory_name]
            territory.ruler = player1.name
            territory.troops = 1
            Logger.log(f'Territory {territory} taken by {player1}', verbose)
        for card in neutral_cards:
            territory = self.state.board.territories[card.territory_name]
            territory.troops = 1
            Logger.log(f'Territory {territory} taken by neutrals', verbose)

        if plot_verbose:
            self.state.board.plot()

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
