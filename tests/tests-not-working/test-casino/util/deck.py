import pythoness
from . import card


class Deck:
    "Represents a deck of cards"

    @pythoness.spec(
        "Creates a standard deck of 52 cards", related_objs=[card.Card], verbose=True
    )
    def __init__(self):
        """"""

    @pythoness.spec(
        "draws a card from the deck, returning it and removing it from the deck",
        related_objs=[__init__],
        verbose=True,
    )
    def draw_card(self):
        """"""

    @pythoness.spec(
        "shuffles the deck, randomizing the order of cards within it",
        related_objs=[__init__],
        verbose=True,
    )
    def shuffle_deck(self):
        """"""
