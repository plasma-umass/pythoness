# file: src/oracle30.py:4-26
# asked: {"lines": [4, 5, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26], "branches": [[6, 7], [6, 9], [14, 15], [14, 26], [17, 18], [17, 23], [20, 21], [20, 22], [23, 14], [23, 24]]}
# gained: {"lines": [4, 5, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26], "branches": [[6, 7], [6, 9], [14, 15], [14, 26], [17, 18], [17, 23], [20, 21], [20, 22], [23, 14], [23, 24]]}

import pytest
from src.oracle30 import Solution

@pytest.fixture
def solution():
    return Solution()

def test_find_substring_empty_string(solution):
    assert solution.findSubstring("", ["foo", "bar"]) == []

def test_find_substring_empty_words(solution):
    assert solution.findSubstring("foobar", []) == []

def test_find_substring_no_match(solution):
    assert solution.findSubstring("foobar", ["baz"]) == []

def test_find_substring_single_match(solution):
    assert solution.findSubstring("barfoothefoobarman", ["foo", "bar"]) == [0, 9]

def test_find_substring_multiple_matches(solution):
    assert solution.findSubstring("wordgoodgoodgoodbestword", ["word", "good", "best", "word"]) == []

def test_find_substring_partial_overlap(solution):
    assert solution.findSubstring("barfoofoobarthefoobarman", ["bar", "foo", "the"]) == [6, 9, 12]

def test_find_substring_exact_match(solution):
    assert solution.findSubstring("wordgoodgoodgoodbestword", ["good", "good", "best", "word"]) == [8]

def test_find_substring_with_repeated_words(solution):
    assert solution.findSubstring("lingmindraboofooowingdingbarrwingmonkeypoundcake", ["fooo", "barr", "wing", "ding", "wing"]) == [13]

