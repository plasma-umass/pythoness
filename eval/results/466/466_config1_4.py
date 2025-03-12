import pythoness
from typing import List, Optional

def getMaxRepetitions(s1: str, n1: int, s2: str, n2: int) -> int:
    """
    We define str = [s, n] as the string str which consists of the string s concatenated n times.

    For example, str == ["abc", 3] =="abcabcabc".

    We define that string s1 can be obtained from string s2 if we can remove some characters from s2 such that it becomes s1.

    For example, s1 = "abc" can be obtained from s2 = "abdbec" based on our definition by removing the bolded underlined characters.

    You are given two strings s1 and s2 and two integers n1 and n2. You have the two strings str1 = [s1, n1] and str2 = [s2, n2].
    Return the maximum integer m such that str = [str2, m] can be obtained from str1.

    Constraints:

    1 <= s1.length, s2.length <= 100
    s1 and s2 consist of lowercase English letters.
    1 <= n1, n2 <= 10^6
    """
    if n1 == 0:
        return 0
    count1 = 0  # count of complete s1 cycles
    count2 = 0  # count of complete s2 cycles
    index2 = 0  # current index in s2
    mapping = {}  # to store previously seen states
    while count1 < n1:
        count1 += 1
        for char in s1:
            if char == s2[index2]:
                index2 += 1
                if index2 == len(s2):
                    index2 = 0
                    count2 += 1
        # Check for repetition
        if index2 in mapping:
            (previous_count1, previous_count2) = mapping[index2]
            cycle_length = count1 - previous_count1
            cycle_count2 = count2 - previous_count2
            remaining_cycles = (n1 - count1) // cycle_length
            count1 += remaining_cycles * cycle_length
            count2 += remaining_cycles * cycle_count2
        else:
            mapping[index2] = (count1, count2)
    return count2 // n2
getMaxRepetitions(s1='acb', n1=4, s2='ab', n2=2)