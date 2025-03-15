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
    maxHeap = []  # A max heap to store the fuel amounts at stations we've passed
    currentFuel = startFuel  # Initial fuel
    previousPosition = 0  # Start position
    refuelStops = 0  # Number of refuels
    for (position, fuel) in stations + [(target, 0)]:
        currentFuel -= position - previousPosition
        while maxHeap and currentFuel < 0:  # Need more fuel to reach this position
            currentFuel += -heapq.heappop(maxHeap)  # Refuel with the largest amount of available fuel
            refuelStops += 1
        if currentFuel < 0:  # Cannot reach this station
            return -1
        heapq.heappush(maxHeap, -fuel)  # Add this station's fuel to our choices
        previousPosition = position
    return refuelStops
minRefuelStops(target=1, startFuel=1, stations=[])