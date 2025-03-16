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

    def count_s2_in_s1(s1: str, s2: str) -> int:
        count = 0
        index_s2 = 0
        for char in s1:
            if char == s2[index_s2]:
                index_s2 += 1
                if index_s2 == len(s2):
                    count += 1
                    index_s2 = 0
        return count
    count1 = count_s2_in_s1(s1, s2)
    if count1 == 0:
        return 0
    total_s1 = n1 * count1
    return total_s1 // (n2 * count_s2_in_s1(s2, s2))
getMaxRepetitions(s1='acb', n1=4, s2='ab', n2=2)