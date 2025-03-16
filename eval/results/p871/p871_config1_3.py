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
    # Add a final destination as a 'station' with 0 additional fuel
    stations.append([target, 0])
    max_heap = []  # Max heap to store fuel capacities others in our path
    (num_refuels, prev_position, current_fuel) = (0, 0, startFuel)
    for (position, fuel) in stations:
        # Travel to the current station
        current_fuel -= position - prev_position
        # While current fuel is negative and there is something in the heap to refuel
        while max_heap and current_fuel < 0:
            current_fuel += -heapq.heappop(max_heap)
            num_refuels += 1
        # If still can't reach current station
        if current_fuel < 0:
            return -1
        # Push current station's fuel to max_heap (invert to simulate max-heap)
        heapq.heappush(max_heap, -fuel)
        prev_position = position
    return num_refuels
minRefuelStops(target=1, startFuel=1, stations=[])