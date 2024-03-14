import random
import sys


def initialise_deck(first_num, last_num, num):
    """Creates a deck of cards from numbers 'first_num' to 'last_num', with each number present 'num' times."""
    deck = [number for number in range(first_num, last_num + 1) for _ in range(num)]
    return deck


def shuffled_deck(lst):
    """Shuffles the deck of cards using the Fisher-Yates Shuffle algorithm."""
    #random.seed(10)  # uncomment the random seed to get the same output every time
    last_index = len(lst) - 1
    while last_index > 0:
        rand_index = random.randint(0, last_index)
        temp = lst[last_index]
        lst[last_index] = lst[rand_index]
        lst[rand_index] = temp
        last_index -= 1
    return lst


def draw_cards_player(player_draw_deck, player_discard_deck):
    """Draw the first card from the list of draw deck"""
    if len(player_draw_deck) != 0:
        return player_draw_deck.pop(0)


def compare_cards(card1, card2):
    """Compare two cards and returns the winners index (0 or 1) or -1 if both cards are the same"""
    if card1 > card2:
        return 0

    elif card2 > card1:
        return 1

    elif card1 == card2:
        return -1


def condition_check(player_draw_deck, player_discard_deck):
    """Checks if draw deck is empty then shuffle discard deck into draw deck"""
    if len(player_draw_deck) == 0:
        if len(player_discard_deck) != 0:
            player_draw_deck.extend(shuffled_deck(player_discard_deck))
            player_discard_deck.clear()
    return player_draw_deck, player_discard_deck


count = 0


def play_turn(player1_draw_deck, player1_discard_deck, player2_draw_deck, player2_discard_deck, tied_cards):
    global count
    player1_draw_deck, player1_discard_deck = condition_check(player1_draw_deck, player1_discard_deck)
    player2_draw_deck, player2_discard_deck = condition_check(player2_draw_deck, player2_discard_deck)

    if (len(player1_draw_deck) + len(player1_discard_deck)) == 0:
        print("Player 2 wins the game!")
        sys.exit()

    if (len(player2_draw_deck) + len(player2_discard_deck)) == 0:
        print("Player 1 wins the game!")
        sys.exit()

    print(f"Player 1 ({len(player1_draw_deck) + len(player1_discard_deck)} cards): {player1_draw_deck[0]}")
    print(f"Player 2 ({len(player2_draw_deck) + len(player2_discard_deck)} cards): {player2_draw_deck[0]}")

    # Draw first card
    player1_draw_card = draw_cards_player(player1_draw_deck, player1_discard_deck)
    player2_draw_card = draw_cards_player(player2_draw_deck, player2_discard_deck)

    result = compare_cards(player1_draw_card, player2_draw_card)

    if result == 0:
        print(f"Player 1 wins this round\n")
        player1_discard_deck.append(player1_draw_card)
        player1_discard_deck.append(player2_draw_card)
        if tied_cards:
            player1_discard_deck.extend(tied_cards)
            tied_cards.clear()
            count -= 1

    elif result == 1:
        print(f"Player 2 wins this round\n")
        player2_discard_deck.append(player1_draw_card)
        player2_discard_deck.append(player2_draw_card)
        if tied_cards:
            player2_discard_deck.extend(tied_cards)
            tied_cards.clear()
            count -= 1

    else:
        print(f"No winner in this round\n")
        tied_cards.append(player1_draw_card)
        tied_cards.append(player2_draw_card)

        count += 1
        if count == 4:
            print(f"Stalemate, game draw!")
            sys.exit()

    return tied_cards


def main():
    # Initialize the deck of cards
    deck = initialise_deck(1, 10, 4)

    # Shuffle the deck of cards
    shuffled_cards = shuffled_deck(deck)
    print(f"Initial shuffled cards:", shuffled_cards)
    print("\n")

    # Distribute 20 cards in each draw deck
    # Initially discard deck is empty for both players
    half_length = int(len(shuffled_cards) / 2)
    player1_draw_deck = shuffled_cards[:half_length]
    player2_draw_deck = shuffled_cards[half_length:]
    player1_discard_deck = []
    player2_discard_deck = []
    tied_cards = []


    while (((len(player1_draw_deck) + len(player1_discard_deck)) != 0) or (
            (len(player1_draw_deck) + len(player1_discard_deck)) != 0)):
        tied_cards = play_turn(player1_draw_deck, player1_discard_deck, player2_draw_deck, player2_discard_deck,
                               tied_cards)

    if len(player1_draw_deck) == 0:
        print(f"Player 2 wins the game!")
    else:
        print(f"Player 1 wins the game!")

if __name__ == "__main__":
    main()
