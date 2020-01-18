import random
from card import Card, CardType
from logger import Logger


class Game:

    def __init__(self, state):
        self.state = state
        self.starter = None
        self.winner = None
        self.move_count = 0

    @staticmethod
    def dice_roll():
        return random.randint(1, 6)

    def assign_cards(self):
        self.state.pile.remove_card_with_index(0)
        self.state.pile.remove_card_with_index(0)
        # cheating until better implementation
        self.state.pile.shuffle()
        player0_cards = self.state.pile[:14]
        player1_cards = self.state.pile[14:28]
        neutral_cards = self.state.pile[28:42]
        for card in player0_cards:
            territory = self.state.board.territories[card.territory_name]
            territory.ruler = self.state.players[0]
            territory.troops = 1
            territory.fill_color = self.state.board.territory_colors[0]
            Logger.log(f'Territory {territory} taken by {self.state.players[0]}', self.state.verbose)
        for card in player1_cards:
            territory = self.state.board.territories[card.territory_name]
            territory.ruler = self.state.players[1]
            territory.troops = 1
            territory.fill_color = self.state.board.territory_colors[1]
            Logger.log(f'Territory {territory} taken by {self.state.players[1]}', self.state.verbose)
        for card in neutral_cards:
            territory = self.state.board.territories[card.territory_name]
            territory.troops = 1
            territory.fill_color = self.state.board.territory_colors[2]
            Logger.log(f'Territory {territory} taken by neutrals', self.state.verbose)

        self.state.board.plot('after_init_step4.png', self.state.display_plot)

    def reinforce_initial_territories(self):
        # Players have 22 troops remaining each.
        for _ in range(11):
            for i in range(2):
                self.state.players[i].reinforce_owned_territory(self.state)
                self.state.players[i].reinforce_owned_territory(self.state)
                self.state.players[i].reinforce_neutral_territory(self.state)
                self.state.player_to_move, self.state.player_to_wait = \
                    self.state.player_to_wait, self.state.player_to_move

        self.state.board.plot('after_init_step5.png', self.state.display_plot)

    def execute_setup(self):
        Logger.log("Initializing setup phase...", self.state.verbose)
        # 1) decide the first player to move based on dice roll
        while True:
            dice_roll_0 = Game.dice_roll()
            Logger.log(f'Player {self.state.players[0]} rolls a {dice_roll_0}', self.state.verbose)
            dice_roll_1 = Game.dice_roll()
            Logger.log(f'Player {self.state.players[1]} rolls a {dice_roll_1}', self.state.verbose)
            if dice_roll_0 == dice_roll_1:
                Logger.log('It\'s a draw! Throwing dice again...', self.state.verbose)
            else:
                maxi_player = int(dice_roll_0 < dice_roll_1)
                break

        # 2) reorder players based on the first to move
        self.reorder_players_by_next_to_move(maxi_player)
        self.starter = self.state.players[0]
        self.state.player_to_move = self.state.players[0]
        self.state.player_to_wait = self.state.players[1]
        Logger.log(f'Player to start: {self.state.players[0]}', self.state.verbose)

        # 3)
        # " Remove the Secret Mission cards and the 2 “wild” cards from the RISK card deck.
        #   Shuffle thoroughly and deal the cards, face down, into 3 equal piles.
        #   Both you and your opponent choose a different pile. The remaining pile is neutral. "
        #
        # 4)
        # " Place one of your Infantry onto each of the 14 territories shown on the RISK cards in your pile.
        #   Your opponent does the same.
        #   Then place one “neutral” Infantry onto each of the remaining 14 “neutral” territories. "
        self.assign_cards()

        # 5)
        # " After every territory on the board has been claimed,
        #   you and your opponent take turns placing your remaining armies:
        #   Place 2 Infantry onto any 1 or 2 of the territories you occupy.
        #   Then place 1 “neutral” army onto any “neutral” territory you want,
        #   placing it to block your opponent’s possible advance. "
        self.reinforce_initial_territories()

        # 6)
        # " After all the armies have been placed on the board,
        #   return the two “wild” cards to the RISK card deck,
        #   shuffle the deck and start to play. "
        self.state.pile.add_card(Card(None, CardType.WILDCARD))
        self.state.pile.add_card(Card(None, CardType.WILDCARD))
        self.state.pile.shuffle()
        Logger.log('Shuffling cards...\nSetup over.', self.state.verbose)

    def play_game(self):
        Logger.log('Starting game...', self.state.verbose)
        move_count = 0
        while not self.over():
            # take turn
            self.state.player_to_move.take_turn(self.state)
            move_count += 1
            if move_count % 10 == 0:
                self.state.board.plot(f'after_turn_{move_count}.png', self.state.display_plot)
            # change players' state
            self.state.player_to_move, self.state.player_to_wait = \
                self.state.player_to_wait, self.state.player_to_move

        self.find_winner()
        self.move_count = move_count
        Logger.log(f'Game finished after {move_count} moves.\n', self.state.verbose)
        Logger.log(f'The winner is {self.winner}!!!', self.state.verbose)
        self.state.board.plot('game_finished.png', self.state.display_plot)

    def reorder_players_by_next_to_move(self, next_player_index):
        self.state.players = self.state.players[next_player_index:] + self.state.players[:next_player_index]

    def over(self):
        player0_territories = self.state.board.occupied_territories(self.state.players[0])
        player1_territories = self.state.board.occupied_territories(self.state.players[1])
        return (not player0_territories) or (not player1_territories)

    def find_winner(self):
        player0_territories = self.state.board.occupied_territories(self.state.players[0])
        if player0_territories:
            self.winner = self.state.players[0]
        else:
            self.winner = self.state.players[1]
