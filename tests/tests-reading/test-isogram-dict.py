import pythoness


@pythoness.spec(
    """Find how many lowercase 7-letter isograms are in words/dict.txt. 
                Each word in words/dict.txt is on a separate line. 
                Return an int representing the number of 7-letter isograms."""
)
def find_iso() -> int:
    """"""


print("Running tests: isogram-dict")
assert find_iso() == 6973
print("Tests complete.")
