import unittest
from final_development_challenge.development_challenge import *


class TestCardGame(unittest.TestCase):

    def setUp(self):
        # Set up initial conditions for the tests
        self.initial_deck = initialise_deck(1, 10, 4)
        self.shuffled_deck = shuffled_deck(self.initial_deck.copy())

    # A new deck should contain 40 cards
    def test_initial_deck_size(self):
        self.assertEqual(len(self.initial_deck), 40)

    # A shuffled deck should contain 40 cards
    def test_shuffled_deck(self):
        self.assertEqual(len(self.shuffled_deck), 40)

    # two lists have same elements but in a different order
    def test_shuffled_deck_content(self):
        self.assertNotEqual(self.shuffled_deck, self.initial_deck)
        self.assertCountEqual(self.shuffled_deck, self.initial_deck)

    def test_initial_deck_distribution(self):
        # Distribute 20 cards in each draw deck
        half_length = int(len(self.shuffled_deck) / 2)
        player1_draw_deck = self.shuffled_deck[:half_length]
        player2_draw_deck = self.shuffled_deck[half_length:]
        player1_discard_deck = []
        player2_discard_deck = []
        tied_cards = []

        # Check if the lengths are correct
        self.assertEqual(len(player1_draw_deck), 20)
        self.assertEqual(len(player2_draw_deck), 20)
        self.assertEqual(len(player1_discard_deck), 0)
        self.assertEqual(len(player2_discard_deck), 0)
        self.assertEqual(len(tied_cards), 0)

        # Check if cards are distributed correctly
        self.assertCountEqual(player1_draw_deck + player1_discard_deck, self.shuffled_deck[:half_length])
        self.assertCountEqual(player2_draw_deck + player2_discard_deck, self.shuffled_deck[half_length:])

    def test_draw_cards(self):
        # to test the first card is drawn from the list
        player_draw_deck = [1, 2, 3, 4, 5]
        player_discard_deck = [6, 7, 8, 9, 10]

        drawn_card = draw_cards_player(player_draw_deck, player_discard_deck)

        self.assertEqual(drawn_card, 1)
        self.assertEqual(player_draw_deck, [2, 3, 4, 5])
        self.assertEqual(player_discard_deck, [6, 7, 8, 9, 10])

    def test_condition_check(self):
        # If a player with an empty draw pile tries to draw a card, the discard pile is shuffled into the draw pile
        # and then discard pile is empty afterwards

        player1_draw_deck = []
        player1_discard_deck = [2, 3, 9, 7]
        player2_draw_deck = []
        player2_discard_deck = [8, 9]
        tied_cards = []

        self.assertEqual(len(player1_draw_deck), 0)
        self.assertNotEqual(len(player1_discard_deck), 0)

        player1_draw_deck, player1_discard_deck = condition_check(player1_draw_deck, player1_discard_deck)
        self.assertEqual(len(player1_draw_deck), 4)
        self.assertEqual(len(player1_discard_deck), 0)

    def test_play_turn_equal_case(self):
        # When comparing two cards of the same value, the winner of the next round should win 4 cards
        player1_draw_deck = [6, 7, 4]
        player1_discard_deck = [2, 3]
        player2_draw_deck = [6, 3, 9]
        player2_discard_deck = [8, 9]
        tied_cards = []

        self.assertEqual(tied_cards, [])

        tied_cards = play_turn(player1_draw_deck, player1_discard_deck, player2_draw_deck, player2_discard_deck,
                               tied_cards)
        self.assertEqual(player1_draw_deck, [7, 4])
        self.assertEqual(player1_discard_deck, [2, 3])
        self.assertEqual(player2_draw_deck, [3, 9])
        self.assertEqual(player2_discard_deck, [8, 9])
        self.assertEqual(tied_cards, [6, 6])

        tied_cards = play_turn(player1_draw_deck, player1_discard_deck, player2_draw_deck, player2_discard_deck,
                               tied_cards)
        self.assertEqual(player1_draw_deck, [4])
        self.assertEqual(player1_discard_deck, [2, 3, 7, 3, 6, 6])
        self.assertEqual(player2_draw_deck, [9])
        self.assertEqual(player2_discard_deck, [8, 9])
        self.assertEqual(tied_cards, [])

    def test_play_turn_normal_case(self):
        # When comparing two cards of the same value, the winner of the next round should win 4 cards
        # Round 1
        player1_draw_deck = [7, 4, 6]
        player1_discard_deck = [2, 3]
        player2_draw_deck = [3, 9, 1]
        player2_discard_deck = [8, 9]
        tied_cards = []

        self.assertEqual(tied_cards, [])

        tied_cards = play_turn(player1_draw_deck, player1_discard_deck, player2_draw_deck, player2_discard_deck,
                               tied_cards)
        self.assertEqual(player1_draw_deck, [4, 6])
        self.assertEqual(player1_discard_deck, [2, 3, 7, 3])
        self.assertEqual(player2_draw_deck, [9, 1])
        self.assertEqual(player2_discard_deck, [8, 9])
        self.assertEqual(tied_cards, [])


    def test_compare_cards(self):
        # When comparing two cards, the higher card player should win

        self.assertEqual(compare_cards(9, 4), 0)  # Player1 wins
        self.assertEqual(compare_cards(7, 8), 1)  # Player2 wins
        self.assertEqual(compare_cards(4, 4), -1)  # No winner
