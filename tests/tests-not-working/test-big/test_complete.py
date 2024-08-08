"""
Module to implement a result object that will be returned by auto complete
"""
import pythoness

class Result:
    """
    A class for outputting readable autocomplete suggestions
    """

    __slots__ = ["_input", "_completions"]

    def __init__(self, inputWord, completionList):
        """
        Constructor for the Result class
        """ 
        self._input = inputWord
        self._completions = completionList


    def __str__(self):
        """
        A method that converts an instance of the Result
        class into an easily readable string.

        >>> print(Result("the", [FreqWord("the",4), FreqWord("theirs",3), FreqWord("then",2)]))
        the --> the[4] | theirs[3] | then[2]
        >>> print(Result('wel', [FreqWord('well', 5), FreqWord('weld', 4), FreqWord('wells', 3)]))
        wel --> well[5] | weld[4] | wells[3]
        """
        # for every word in the completions list, make it into our desired string
        # and removethe extra ' | ' from the end 
        results = str(self._input) + ' --> '
        for word in self._completions: 
            results += str(word) + ' | '
        return results.strip(' | ')

"""
A module for representing information about words in a corpus.
"""

class FreqWord:
    """
    A class representing a word and its count.
    """

    # _text is a string, _count is an int
    __slots__ = ["_text", "_count"]

    def __init__(self, text, count):
        """
        Constructor for the FreqWord class.
        """
        self._text = text
        self._count = int(count)

    def __eq__(self, other):
        if isinstance(other, FreqWord): 
            if other._text == self._text and other._count == self._count: 
                return True
        return False

    def getText(self):
        """
        Accessor method to get text of the word

        >>> FreqWord('contemplate', 100).getText()
        'contemplate'
        >>> FreqWord('', 0).getText()
        ''
        >>> FreqWord('1345', 5).getText()
        '1345'
        >>> FreqWord('UPPER', 3).getText()
        'UPPER'
        """
        return self._text

    def getCount(self):
        """
        Accessor method to get frequency of the word

        >>> FreqWord('contemplate', 100).getCount()
        100
        >>> FreqWord('', 0).getCount()
        0
        >>> FreqWord('UPPER', -1).getCount()
        -1
        """
        return self._count

    def __str__(self):
        """
        A method that converts an instance of the FreqWord
        class into an easily readable string.

        >>> print(FreqWord("moo", 5))
        moo[5]
        >>> print(FreqWord(' ', 0))
         [0]
        >>> print(FreqWord('UPPER', -1))
        UPPER[-1]
        """
        # Formatting in the way it wants via concatenation
        return self._text + '[{}]'.format(self._count)


    def hasPrefix(self, prefix):
        """
        Returns whether the text starts with the given prefix or not.

        >>> FreqWord('contemplate', 100).hasPrefix('con')
        True
        >>> FreqWord('contemplate', 100).hasPrefix('tempt')
        False
        >>> FreqWord('cone', 100).hasPrefix('one')
        False
        >>> FreqWord('provost', 5).hasPrefix('provos')
        True
        """
        return self._text.startswith(prefix)


    def __repr__(self):
        """
        This is a special method that helps Python print lists 
        of FreqWord objects in a nice way.  DO NOT MODIFY 
        this method.
        """
        # Just invoke the __str__ method to create a nice string.
        return self.__str__()


    def matchesPattern(self, pattern):
        """
         Returns whether the text matches the given pattern or not.
    
        >>> FreqWord('contemplate', 100).matchesPattern('c***emp*at*')
        True
        >>> FreqWord('contemplate', 100).matchesPattern('contemp**')
        False
        >>> FreqWord('test', 100).matchesPattern('text')
        False
        >>> FreqWord('test', 100).matchesPattern('ne*t')
        False
        >>> FreqWord(' ', 100).matchesPattern('**')
        False
        """
        i = 0
        # go through every letter in the pattern
        # if the lengths are unequal, stop immediately
        # then check if every letter is equal in pattern and self is equal
        # or if that letter is an asterisk
        # if all letters match, while loop ends and returns True, else, return False
        while i < len(pattern):
            if len(self._text) == len(pattern) and (pattern[i] == self._text[i] or pattern[i] == '*'):
                i += 1
            else: 
                return False
        return True


# The following two *functions* are defined outside of the class, 
# so that we can use them as the key functions when sorting.

@pythoness.spec("""A function that can be used as a sorting key function
                It extracts the text from FreqWords""",
                tests=["sorted([ FreqWord('b',5), FreqWord('c',10), FreqWord('a', 8) ],key=textKey) == [FreqWord('a',8), FreqWord('b',5), FreqWord('c',10)]"],
                related_objs='*', verbose=True)
def textKey(freqWord):
    ""
    

def countKey(freqWord):
    """
    A function that can be used as a sorting key function.
    It extracts the count from FreqWords.

    >>> words = [ FreqWord("b",5), FreqWord("c",10), FreqWord("a", 8) ]
    >>> sorted(words, key = countKey)
    [b[5], a[8], c[10]]
    >>> sorted(words, key = countKey, reverse = True)
    [c[10], a[8], b[5]]
    """
    # return only count
    return freqWord.getCount()

"""
Module to implement auto complete
"""

class AutoComplete:
    """
    A class for generating autocomplete suggestions
    """

    __slots__ = [ "_words" ]

    @pythoness.spec("""Constructor for the AutoComplete class. The input
        corpus corresponds to a filename (string) to be used as 
        a basis for constructing the frequency of words list. Sort using textKey.""",
        tests=["AutoComplete('data/miniGutenberg.csv')._words[0]==FreqWord('circumstances',107)",
               "AutoComplete('data/miniGutenberg.csv')._words[-2]==FreqWord('wooded',8)",
               "AutoComplete('data/miniGutenberg.csv')._words[-2].getText()=='wooded'",
               "AutoComplete('data/miniGutenberg.csv')._words[-2].getCount()==8"], related_objs='*', verbose=True, e_print=True)
    def __init__(self, corpus):
        ""


    def _matchWords(self, criteria):
        """
        Part 3 of Lab:
        Perform a search to return a list of word objects that match
        the given criteria -- when the criteria corresponds to a prefix,
        this returns a list where each word contains the given prefix.

        Part 4 of Lab:
        if the criteria corresponds to a pattern (contains *'s), this
        returns a list where each word matches the given pattern.

        >>> AutoComplete("data/miniGutenberg.csv")._matchWords("sc")
        [scold[3], scraped[21]]
        >>> AutoComplete("data/miniGutenberg.csv")._matchWords("um")
        []
        """
        # if it has asterisks (wildcards), run matchesPattern and make the list
        # otherwise, run hasPrefix instead and make the list
        if '*' in criteria: 
            matchWords = [word for word in self._words if word.matchesPattern(criteria)]
        else: 
            matchWords = [word for word in self._words if word.hasPrefix(criteria)]
        return matchWords


    def suggestCompletions(self, inputString):
        """
        Suggest word completions based on (i) whether the user has 
        input a criteria or a wild card expression and (ii) frequency 
        of occurrence of the possible completions. The final object 
        that is returned is an instance of the Result class with the 
        top 3 completions if at least 3 possible completions exist 
        (and fewer if there are less than 3 possible completions.) 
        
        *WE DID THE EXTENSION WHERE IF THE WORD EXACTLY MATCHES, 
        IT APPEARS FIRST IN THE RESULT*

        >>> print(AutoComplete("data/gutenberg.csv").suggestCompletions("auto"))
        auto --> auto[3] | autonomy[7] | autocratic[5]
        >>> print(AutoComplete('data/gutenberg.csv').suggestCompletions('Jeannie').strip())
        Jeannie -->
        >>> print(AutoComplete("data/miniGutenberg.csv").suggestCompletions("woo*e*"))
        woo*e* --> wooden[37] | wooded[8]
        >>> print(AutoComplete("data/gutenberg.csv").suggestCompletions("woo*e*"))
        woo*e* --> wooden[37] | woolen[15] | wooded[8]
        """
        # make a list of matching words
        # sort them using the countKey, backwards so it's in descending order
        # return the Result of the first three (or fewer) items in the completions list
        completions = self._matchWords(inputString)
        completions = sorted(completions, key = countKey, reverse = True)
        
        # *EXTRA CREDIT PART*
        # if the input string exactly matches one of our freqWords in completions
        # remove it from the list and put it back at index 0
        for freqWord in completions:
            if inputString == freqWord._text:
                completions.remove(freqWord)
                completions.insert(0, freqWord)
        
        return str(Result(inputString, completions[0:3]))

    def __str__(self):
        """
        >>> print(AutoComplete("data/miniGutenberg.csv"))
        circumstances[107]
        scold[3]
        scraped[21]
        wooded[8]
        wooden[37]
        """
        # print out each of the words with a new line
        # strip the new line once it's all done
        finalStr = ""
        for FreqWord in self._words: 
            finalStr += str(FreqWord) + '\n'
        return finalStr.strip()
        

if __name__ == "__main__":
    # Run all the doctests
    # import doctest
    # doctest.testmod()

    # Suggest completions for any input strings provided on the command
    # line.  Eg:
    #
    #    python3 autocomplete.py moo cow r***s
    #
    import sys
    # print(type(AutoComplete('data/miniGutenberg.csv')._words[-2].getCount()))
    # print(type(sorted([ FreqWord('b',5), FreqWord('c',10), FreqWord('a', 8) ], key = countKey)))

    # print(sorted([ FreqWord('b',5), FreqWord('c',10), FreqWord('a', 8) ], key = countKey))
    # print(sorted([ FreqWord('b',5), FreqWord('c',10), FreqWord('a', 8) ], key = countKey)[0])
    # print(type(sorted([ FreqWord('b',5), FreqWord('c',10), FreqWord('a', 8) ], key = countKey)[0]))

    

    print(AutoComplete('data/miniGutenberg.csv')._words[0])

    # auto = AutoComplete("data/gutenberg.csv")
# 
    # for inputString in sys.argv[1:]:
    #     print(auto.suggestCompletions(inputString))
