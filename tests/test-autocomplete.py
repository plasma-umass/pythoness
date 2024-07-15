import pythoness
from freqword import *
from result import *

class AutoComplete:
    """A class for generating autocomplete suggestions"""

    __slots__ = [ "_words" ]

    @pythoness.spec("""Constructor for the AutoComplete class. The input
        corpus corresponds to a filename (string) to be used as 
        a basis for constructing the frequency of words list""",
        tests=["AutoComplete('data/miniGutenberg.csv')._words[0]==circumstances[107]",
               "AutoComplete('data/miniGutenberg.csv')._words[-2]==wooded[8]",
               "AutoComplete('data/miniGutenberg.csv')._words[-2].getText()=='wooded'",
               "AutoCopmlete('data/miniGutenberg.csv')._words[-2].getCount()==8)"])
    def __init__(self, corpus):
        ""

    @pythoness.spec("""Perform a search to return a list of word objects that match
        the given criteria -- when the criteria corresponds to a prefix,
        this returns a list where each word contains the given prefix.

        if the criteria corresponds to a pattern (contains *'s), this
        returns a list where each word matches the given pattern.""",
        tests=["AutoComplete('data/miniGutenberg.csv')._matchWords('sc')==[scold[3], scraped[21]]",
               "AutoComplete('data/miniGutenberg.csv')._matchWords('um')==[]"])
    def _matchWords(self, criteria):
        ""

    @pythoness.spec("""Suggest word completions based on (i) whether the user has 
        input a criteria or a wild card expression and (ii) frequency 
        of occurrence of the possible completions. The final object 
        that is returned is an instance of the Result class with the 
        top 3 completions if at least 3 possible completions exist 
        (and fewer if there are less than 3 possible completions.)

        Here is an example of using this function with print():
        print(AutoComplete("data/gutenberg.csv").suggestCompletions("auto")) == auto --> auto[3] | autonomy[7] | autocratic[5]
        """)
    def suggestCompletions(self, inputString):
        ""

    @pythoness.spec("""Converts AutoComplete results into the following format:
                    circumstances[107]
                    scold[3]
                    scraped[21]""")
    def __str__(self):
        ""