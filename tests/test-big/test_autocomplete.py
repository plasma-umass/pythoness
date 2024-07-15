import pythoness
from test_freqword import *
from test_result import *

class Result:
    """A Class for outputting readable autocomplete suggestions"""

    __slots__ = ["_input", "_completions"]

    @pythoness.spec("Constructor for the result class",related_objs='*', verbose=True)
    def __init__(self, inputWord, completionList):
        ""

    @pythoness.spec("""A method that convers an instance of the Result class 
                    into an easily reable string
                    
                    here's an axamlpe format:
                    print(Result("the", [FreqWord("the",4), FreqWord("theirs",3), FreqWord("then",2)])) ==
                    the --> the[4] | theirs[3] | then[2]
                    """,related_objs='*', verbose=True)
    def __str__(self):
        ""

class FreqWord:
    """
    A class representing a word and its count
    """

    __slots__ = ["_text", "_count"]

    @pythoness.spec("""
                    Constructor for the FreqWord class.
                    """, related_objs='*', verbose=True)
    def __init__(self, text, count):
        ""

    @pythoness.spec("Accessor method to get text of the word", 
                    tests=["FreqWord('contemplete', 100).getText()=='contemplate'","FreqWord('', 0).getText()==''",
                           "FreqWord('1345', 5).getText()=='1345'","FreqWord('UPPER', 3).getText()=='UPPER'"],
                           related_objs='*', verbose=True)
    def getText(self):
        ""

    @pythoness.spec("Accessor method to get frequencyt of the word",
                    tests=["FreqWord('contemplate', 100).getCount()==100","FreqWord('', 0).getCount()==0",
                           "FreqWord('UPPER', -1).getCount()==-1"],
                           related_objs='*', verbose=True)
    def getCount(self):
        ""

    @pythoness.spec("""
                    A method that converts an instance of the FreqWord class
                    into an easily readable string.
                    
                    For example: print(FreqWord("moo",5)) -> moo[5]""",
                    related_objs='*', verbose=True)
    def __str__(self):
        ""

    @pythoness.spec("Returns whteher the text starts with the given prefix or not",
                    tests=["FreqWord('contemplate', 100).hasPrefix('con')==True",
                           "FreqWord('contemplate', 100).hasPrefix('tempt')==False",
                           "FreqWord('cone', 100).hasPrefix('one')==False",
                           "FreqWord('provost', 5).hasPrefix('provos')==True"],
                           related_objs='*', verbose=True)
    def hasPrefix(self, prefix):
        ""

    def __repr__(self):
        """
        This is a special method that helps Python print lists 
        of FreqWord objects in a nice way.  DO NOT MODIFY 
        this method.
        """
        # Just invoke the __str__ method to create a nice string.
        return self.__str__()
    
    @pythoness.spec("Returns whether the text matches the given pattern or not, where '*', verbose=True represents any character",
                    tests=["FreqWord('contemplate', 100).matchesPattern('c***emp*at*')==True",
                           "FreqWord('contemplate', 100).matchesPattern('contemp**')==False",
                           "FreqWord('test', 100).matchesPattern('text')==False",
                           "FreqWord('test', 100).matchesPattern('ne*t')==False",
                           "FreqWord(' ', 100).matchesPattern('**')==False"],
                           related_objs='*', verbose=True)
    def matchesPattern(self, pattern):
        ""

@pythoness.spec("""A function that can be used as a sorting key function
                It extracts the text from FreqWords""",
                tests=["sorted([ FreqWord('b',5), FreqWord('c',10), FreqWord('a', 8) ],key=textkey) == '[FreqWord('a',8), FreqWord('b',5), FreqWord('c',10)]'"],
                related_objs='*', verbose=True)
def textKey(freqWord):
    ""


@pythoness.spec("""A function that can be used as a sorting key function
                It extracts the count from FreqWords""",
                tests=["sorted([ FreqWord('b',5), FreqWord('c',10), FreqWord('a', 8) ], key = countKey)=='[FreqWord('b',5), FreqWord('a',8), FreqWord('c',10)]'"],
                related_objs='*', verbose=True)
def countKey(freqWord):
    ""

class AutoComplete:
    """A class for generating autocomplete suggestions"""

    __slots__ = [ "_words" ]

    @pythoness.spec("""Constructor for the AutoComplete class. The input
        corpus corresponds to a filename (string) to be used as 
        a basis for constructing the frequency of words list""",
        tests=["AutoComplete('data/miniGutenberg.csv')._words[0]==FreqWord('circumstances',107)",
               "AutoComplete('data/miniGutenberg.csv')._words[-2]==FreqWord('wooded',8)",
               "AutoComplete('data/miniGutenberg.csv')._words[-2].getText()=='wooded'",
               "AutoComplete('data/miniGutenberg.csv')._words[-2].getCount()==8)"], related_objs='*', verbose=True, e_print=True)
    def __init__(self, corpus):
        ""

    @pythoness.spec("""Perform a search to return a list of word objects that match
        the given criteria -- when the criteria corresponds to a prefix,
        this returns a list where each word contains the given prefix.

        if the criteria corresponds to a pattern (contains *'s), this
        returns a list where each word matches the given pattern.""",
        tests=["AutoComplete('data/miniGutenberg.csv')._matchWords('sc')=='[FreqWord('scold',3), FreqWord('scraped',21)]'",
               "AutoComplete('data/miniGutenberg.csv')._matchWords('um')=='[]'"], related_objs='*', verbose=True)
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
        """, related_objs='*', verbose=True)
    def suggestCompletions(self, inputString):
        ""

    @pythoness.spec("""Converts AutoComplete results into the following format:
                    circumstances[107]
                    scold[3]
                    scraped[21]""", related_objs='*', verbose=True)
    def __str__(self):
        ""

if __name__ == "__main__":
    import sys
    auto = AutoComplete("data/gutenberg.csv")
    for inputString in sys.argv[1:]:
        print(auto.suggestCompletions(inputString))