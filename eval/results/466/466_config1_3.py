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
    (len1, len2) = (len(s1), len(s2))
    (index1, index2) = (0, 0)
    (count1, count2) = (0, 0)
    # A dictionary to store the index in s1 where each index of s2 is reset
    index_dict = {}
    while count1 < n1:
        if s1[index1] == s2[index2]:
            index2 += 1
            if index2 == len2:
                index2 = 0
                count2 += 1
            # Store the state of s1 index and repetitions when s2 is reset
            if index2 in index_dict:
                # Cycle detected
                (prev_index1, prev_count1, prev_count2) = index_dict[index2]
                cycle_length = count1 - prev_count1
                cycle_count = count2 - prev_count2
                complete_cycles = (n1 - count1) // cycle_length
                count1 += complete_cycles * cycle_length
                count2 += complete_cycles * cycle_count
            else:
                index_dict[index2] = (index1, count1, count2)
        index1 += 1
        if index1 == len1:
            index1 = 0
            count1 += 1
    return count2 // n2
getMaxRepetitions(s1='acb', n1=4, s2='ab', n2=2)