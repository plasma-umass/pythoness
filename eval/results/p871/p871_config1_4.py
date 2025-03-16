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
    pq = []  # max-heap as a min heap with negated fuel values
    stations.append([target, 0])
    fuel = startFuel
    prev = 0
    result = 0
    for (position, fuel_at_station) in stations:
        fuel -= position - prev
        while pq and fuel < 0:  # while we need more fuel to reach this station
            fuel += -heapq.heappop(pq)  # refuel with the largest available fuel
            result += 1
        if fuel < 0:
            return -1
        heapq.heappush(pq, -fuel_at_station)
        prev = position
    return result
minRefuelStops(target=1, startFuel=1, stations=[])