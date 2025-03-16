import pythoness
from typing import List, Optional

def getMaxRepetitions(s1: str, n1: int, s2: str, n2: int) -> int:
    """
    We define str = [s, n] as the string str which consists of the string s concatenated n times.

    For example, str == ["abc", 3] == "abcabcabc".

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
    # Initialization
    (s1_count, s2_count, index_s2) = (0, 0, 0)
    (length_s1, length_s2) = (len(s1), len(s2))
    # This map will store the index of s2 and the number of s2_count when a specific s1_count is reached
    recall = {}
    while s1_count < n1:
        # Loop through s1
        for char in s1:
            if char == s2[index_s2]:
                index_s2 += 1
                if index_s2 == length_s2:
                    s2_count += 1
                    index_s2 = 0
        s1_count += 1
        # Check for a pattern
        if index_s2 in recall:
            (s1_count_prime, s2_count_prime) = recall[index_s2]
            pre_loop = (s1_count_prime, s2_count_prime)
            in_loop = (s1_count - s1_count_prime, s2_count - s2_count_prime)
            break
        else:
            recall[index_s2] = (s1_count, s2_count)
    else:
        return s2_count // n2
    # After finding a pattern, calculate the result
    rest = (n1 - pre_loop[0]) % in_loop[0]
    in_loop_count = (n1 - pre_loop[0]) // in_loop[0]
    rest_count = 0
    partial_s1_count = pre_loop[0] + in_loop[0] * in_loop_count
    for _ in range(partial_s1_count, partial_s1_count + rest):
        for char in s1:
            if char == s2[index_s2]:
                index_s2 += 1
                if index_s2 == length_s2:
                    rest_count += 1
                    index_s2 = 0
    return (pre_loop[1] + in_loop[1] * in_loop_count + rest_count) // n2
getMaxRepetitions(s1='acb', n1=4, s2='ab', n2=2)