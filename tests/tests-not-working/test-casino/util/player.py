import pythoness


class Player:
    "A player"

    @pythoness.spec("Creates a player object with a bank of value", verbose=True)
    def __init__(self, value):
        """"""

    @pythoness.spec(
        "Gets the current value in the bank of the player",
        related_objs=[__init__],
        verbose=True,
    )
    def get_bank(self):
        """"""

    @pythoness.spec(
        "Adds a value to the bank of a player", related_objs=[__init__], verbose=True
    )
    def add_money(self, value):
        """"""

    @pythoness.spec(
        "Removes a value from the bank of a player",
        related_objs=[__init__, add_money],
        verbose=True,
    )
    def remove_money(self, value):
        """"""
