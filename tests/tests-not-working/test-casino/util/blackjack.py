import pythoness


class Player:
    "A player"

    @pythoness.spec("Creates a player object which stores a hand of cards", verbose=True)
    def __init__(self):
        ""

    @pythoness.spec("Adds a card to the hand of the player", verbose = True)
    def add_card_to_hand(self, card):
        ""

    # @pythoness.spec("Gets the current value in the bank of the player", related_objs=[__init__], verbose=True)
    # def get_bank(self):
    #     ""
    # 
    # @pythoness.spec("Adds a value to the bank of a player", related_objs=[__init__],verbose=True )
    # def add_money(self, value):
    #     ""
    # 
    # @pythoness.spec("Removes a value from the bank of a player", related_objs=[__init__, add_money], verbose=True)
    # def remove_money(self, value):
    #     ""

class Card:
    "Represents a playing card"

    @pythoness.spec("creates a playing card of value (where 11-13 represent face cards) and suit is one of [Hearts, Diamonds, Spades, Clubs]", verbose=True)
    def __init__(self, value, suit):
        ""

    @pythoness.spec("returns a tuple of (value, suit) of the card, where face cards are appropriately named", related_objs=[__init__], verbose=True)
    def get_card(self):
        ""


class Deck:
    "Represents a deck of cards"
    
    @pythoness.spec("Creates a standard deck of 52 cards, stored in self.cards", related_objs=[Card], verbose=True)
    def __init__(self):
        ""

    @pythoness.spec("draws a card from the deck, returning it and removing it from the deck", related_objs=[__init__], verbose=True)
    def draw_card(self):
        ""

    @pythoness.spec("shuffles the deck, randomizing the order of cards within it", related_objs=[__init__], verbose=True)
    def shuffle_deck(self):
        ""



class Blackjack:

    class Blackjack2:
        ""

    # @pythoness.spec("creates a blackjack game, which consists of a player and a deck",related_objs=[Player, Card, Deck], verbose=True)
    def __init__(self):
        ""
        return

    @pythoness.spec("""Plays a blackjack hand, which consists of the following:
                        - create a 2 player objects, one who is the user and one is who is the dealer
                        - the dealer draws two cards from the deck, the first of which is told to the player
                        - the player draws two cards, both of which are visible
                        - the player is repeatedly prompted on whether they would like to hit or stand,
                            until the value of their cards exceed 21 or the player chooses to stand. Face cards are
                            all worth 10, and the aces are worth either 1 or 11, depending on which is optimal.
                            Exceeding 21 represents a loss, and standing while under 21 allows the dealer to play
                        - the dealer chooses to hit until the value of their cards exceeds 16, after which they choose to stand,
                            or loses if their total value exceeds 21
                        - if the dealer loses, the player wins
                        - print the winner
                    """, related_objs=[Player, Card, Deck, __init__], verbose=True)
    def play_hand(self):
        ""

    @pythoness.spec("creates a fresh deck of 52 cards", related_objs=[Player, Card, Deck, __init__], verbose=True)
    def create_deck(self):
        ""

    # @pythoness.spec("The main blackjack logic. Plays 5 hands, then recreates the deck", related_objs=[play_hand, create_deck], verbose=True)
    # def play_game(self):
    #     ""
    
    

