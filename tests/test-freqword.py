import pythoness

class FreqWord:
    """
    A class representing a word and its count
    """

    __slots__ = ["_text", "_count"]

    @pythoness.spec("""
                    Constructor for the FreqWord class.
                    """)
    def __init__(self, text, count):
        ""

    @pythoness.spec("Accessor method to get text of the word", 
                    tests=["FreqWord('contemplete', 100).getText()=='contemplate'","FreqWord('', 0).getText()==''",
                           "FreqWord('1345', 5).getText()=='1345'","FreqWord('UPPER', 3).getText()=='UPPER'"])
    def getText(self):
        ""

    @pythoness.spec("Accessor method to get frequencyt of the word",
                    tests=["FreqWord('contemplate', 100).getCount()==100","FreqWord('', 0).getCount()==0",
                           "FreqWord('UPPER', -1).getCount()==-1"])
    def getCount(self):
        ""

    @pythoness.spec("""
                    A method that converts an instance of the FreqWord class
                    into an easily readable string.
                    
                    Foe example: print(FreqWord("moo",5)) -> moo[5]""")
    def __str__(self):
        ""

    @pythoness.spec("Returns whteher the text starts with the given prefix or not",
                    tests=["FreqWord('contemplate', 100).hasPrefix('con')==True",
                           "FreqWord('contemplate', 100).hasPrefix('tempt')==False",
                           "FreqWord('cone', 100).hasPrefix('one')==False",
                           "FreqWord('provost', 5).hasPrefix('provos')==True"])
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
    
    @pythoness.spec("Returns whether the text matches the given pattern or not, where '*' represents any character",
                    tests=["FreqWord('contemplate', 100).matchesPattern('c***emp*at*')==True",
                           "FreqWord('contemplate', 100).matchesPattern('contemp**')==False",
                           "FreqWord('test', 100).matchesPattern('text')==False",
                           "FreqWord('test', 100).matchesPattern('ne*t')==False",
                           "FreqWord(' ', 100).matchesPattern('**')==False"])
    def matchesPattern(self, pattern):
        ""

@pythoness.spec("""A function that can be used as a sorting key function
                It extracts the text from FreqWords""",
                tests=["sorted([ FreqWord('b',5), FreqWord('c',10), FreqWord('a', 8) ],key=textkey) == [a[8], b[5], c[10]]"])
def textKey(freqWord):
    ""


@pythoness.spec("""A function that can be used as a sorting key function
                It extracts the count from FreqWords""",
                tests=["sorted([ FreqWord('b',5), FreqWord('c',10), FreqWord('a', 8) ], key = countKey)==[b[5], a[8], c[10]]"])
def countKey(freqWord):
    ""