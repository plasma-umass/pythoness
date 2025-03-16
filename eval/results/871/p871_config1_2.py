import pythoness
from typing import List, Optional

def minRefuelStops(target: int, startFuel: int, stations: List[List[int]]) -> int:
    """
    A car travels from a starting position to a destination which is target miles east of the starting position.
    There are gas stations along the way. The gas stations are represented as an array stations where stations[i] = [positioni, fueli] indicates that the i^th gas station is positioni miles east of the starting position and has fueli liters of gas.
    The car starts with an infinite tank of gas, which initially has startFuel liters of fuel in it. It uses one liter of gas per one mile that it drives. When the car reaches a gas station, it may stop and refuel, transferring all the gas from the station into the car.
    Return the minimum number of refueling stops the car must make in order to reach its destination. If it cannot reach the destination, return -1.
    Note that if the car reaches a gas station with 0 fuel left, the car can still refuel there. If the car reaches the destination with 0 fuel left, it is still considered to have arrived.

    Constraints:

    1 <= target, startFuel <= 10^9
    0 <= stations.length <= 500
    1 <= positioni < positioni+1 < target
    1 <= fueli < 10^9
    """
    import heapq
    # Max heap to track the largest fuel at stations we can reach
    max_heap = []
    stations.append((target, 0))  # Append target as the last 'station'
    fuel_stops = 0
    prev_position = 0
    for (position, fuel) in stations:
        startFuel -= position - prev_position  # reduce fuel for the distance traveled
        # While we cannot reach the current station, refuel with the largest available past station
        while max_heap and startFuel < 0:
            startFuel += -heapq.heappop(max_heap)
            fuel_stops += 1
        if startFuel < 0:
            return -1
        # Add current station's fuel to the heap
        heapq.heappush(max_heap, -fuel)
        prev_position = position
    return fuel_stops
minRefuelStops(target=1, startFuel=1, stations=[])