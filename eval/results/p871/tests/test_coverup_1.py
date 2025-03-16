# file: src/oracle871.py:1-20
# asked: {"lines": [1, 2, 9, 11, 12, 13, 14, 16, 17, 18, 20], "branches": [[11, 12], [11, 16], [12, 11], [12, 13], [13, 12], [13, 14], [16, 17], [16, 20], [17, 16], [17, 18]]}
# gained: {"lines": [1, 2, 9, 11, 12, 13, 14, 16, 17, 18, 20], "branches": [[11, 12], [11, 16], [12, 11], [12, 13], [13, 12], [13, 14], [16, 17], [16, 20], [17, 16], [17, 18]]}

import pytest
from src.oracle871 import Solution

def test_minRefuelStops_no_stations():
    sol = Solution()
    assert sol.minRefuelStops(100, 50, []) == -1

def test_minRefuelStops_exact_fuel():
    sol = Solution()
    assert sol.minRefuelStops(100, 100, []) == 0

def test_minRefuelStops_one_station_enough():
    sol = Solution()
    assert sol.minRefuelStops(100, 50, [[50, 50]]) == 1

def test_minRefuelStops_one_station_not_enough():
    sol = Solution()
    assert sol.minRefuelStops(100, 50, [[50, 25]]) == -1

def test_minRefuelStops_multiple_stations():
    sol = Solution()
    assert sol.minRefuelStops(100, 10, [[10, 60], [20, 30], [30, 30], [60, 40]]) == 2

def test_minRefuelStops_multiple_stations_not_enough():
    sol = Solution()
    assert sol.minRefuelStops(100, 10, [[10, 20], [20, 20], [30, 20], [60, 20]]) == -1
