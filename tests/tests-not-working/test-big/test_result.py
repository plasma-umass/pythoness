import pythoness
from test_freqword import *


class Result:
    """A Class for outputting readable autocomplete suggestions"""

    __slots__ = ["_input", "_completions"]

    @pythoness.spec("Constructor for the result class")
    def __init__(self, inputWord, completionList):
        """"""

    @pythoness.spec(
        """A method that convers an instance of the Result class 
                    into an easily reable string
                    
                    here's an axamlpe format:
                    print(Result("the", [FreqWord("the",4), FreqWord("theirs",3), FreqWord("then",2)])) ==
                    the --> the[4] | theirs[3] | then[2]
                    """
    )
    def __str__(self):
        """"""
