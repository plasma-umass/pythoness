import pythoness


def letters(phrase):
    """Takes as input a string phrase and returns a string
    that contains just the letters from phrase (in order).
    """
    result = ""
    for char in phrase:
        # store only the alphabetic characters in result
        if char.isalpha():
            result += char
    return result


def canon(word):
    """Takes as input a string word and returns a "canonical" version
    of word: just the letters, in lower case, and in alphabetical order
    (as a string). Supports anagram testing.
    """

    # get the letters from word, make them lowercase, and sort them
    word = letters(word)
    lowerWord = word.lower()

    # ie.  a *list* of letters, in alpha order
    orderedWord = sorted(lowerWord)

    # convert our list back to a string of characters
    result = "".join(orderedWord)
    return result


def uniques(word):
    """Takes an input string word and return a string consisting of the unique
    characters in word (treating each letter as lowercase and one character).
    """

    # turn the word(s) into lowercase letters and declare a final variable
    word = letters(word)
    word = word.lower()
    charstr = ""

    # compare each letter in the word with each other
    for char1 in word:
        for char2 in word:
            # if the characters are the same AND not already in the list, add it to the string
            if char1 == char2 and char1 not in charstr:
                charstr = charstr + char1

    return charstr


def isIsogram(word):
    """Takes as input a string word and returns True only if the
    characters in word are unique (i.e., there are no repeated characters).
    Note that case should be ignored (i.e., E and e are the same character).
    """
    # turn the word into lowercase letters, find the unique letters, and declare a counting variable
    word = letters(word)
    word = word.lower()
    uniquechars = uniques(word)
    i = 0

    # compare the letters of word with unique characters, and everytime one matches, add 1 to i
    for char1 in word:
        for char2 in uniquechars:
            if char1 == char2:
                i += 1

    # if every character in word has only one match in uniquechars, i and len(uniquechars) will be equal
    # and it is therefore an isogram
    if i == len(uniquechars):
        return True

    # if they aren't equal, a letter matched (appeared) more than once and it isn't an isogram
    else:
        return False


def sized(n, wordList):
    """Takes input of an integer n and a list of string words and returns which words
    in that list have a length of n (not including spaces)
    """
    # declaring variable to store matching words
    matchingWords = []

    # check the letters of every word, and if length is equal to n, include that word on a list
    for word in wordList:
        word = letters(word)
        if len(word) == n:
            matchingWords.append(word)

    return matchingWords


def readWords(filename):
    """Takes as input the path to a file filename, opens and reads the words
    (one per line) in that file, and returns a list containing those words.
    """
    results = []
    with open(filename) as wordFile:
        for line in wordFile:
            word = line.strip()  # do not use letters (think: 'belly button')
            results.append(word)
    return results


@pythoness.spec(
    """In words/diseases.txt is a list of names of diseases and in words/bibleNames.txt
    is a list of bible names.

    Think of a disease in five letters. Shift each letter three
    spaces later in the alphabet---for example, 'a' would become 'd', 'b' would
    become 'e', etc. The result will be a prominent name from the Bible. 
    
    This function returns a string that is a concatenation of the illness and
    the name (eg, 'illness name' or 'name illness').
    """,
    related_objs=[letters, canon, uniques, sized, readWords],
    verbose=True,
    max_retries=10,
)
def p3() -> str:
    """"""


if __name__ == "__main__":
    print("p3(): " + str(p3()))
    # correct answer: Ebola Herod
