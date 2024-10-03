import pythoness


class Card:
    "Represents a playing card"

    @pythoness.spec(
        "creates a playing card of value (where 11-13 represent face cards) and suit is the suit",
        verbose=True,
    )
    def __init__(self, value, suit):
        """"""

    @pythoness.spec(
        "returns a tuple of (value, suit) of the card, where face cards are appropriately named",
        related_objs=[__init__],
        verbose=True,
    )
    def get_card(self):
        """"""
