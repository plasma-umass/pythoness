# file: src/oracle466.py:4-7
# asked: {"lines": [4, 5, 6, 7], "branches": []}
# gained: {"lines": [4, 5, 6, 7], "branches": []}

import pytest
from src.oracle466 import Record

def test_record_initialization():
    record = Record(count=5, nextIndex=10)
    assert record.count == 5
    assert record.nextIndex == 10

def test_record_modification():
    record = Record(count=5, nextIndex=10)
    record.count = 15
    record.nextIndex = 20
    assert record.count == 15
    assert record.nextIndex == 20
