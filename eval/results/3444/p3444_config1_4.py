import pythoness
from typing import List, Optional

class Solution:
    
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        """
        Calculates the minimum number of operations needed to ensure each element in the target array has at least one multiple in the nums array. In each operation, any element in nums can be incremented by 1. The function ensures compliance with constraints on array lengths and element values.
        """
        # The minimum increments required to make nums cover each target
        increments = 0
        # Iterate over each element in the target array
        for t in target:
            # Start assuming the max increments required for each element in target
            min_increment_for_t = float('inf')
            # Check each element in nums for its multiple coverage
            for n in nums:
                # Find the increments needed to make n a multiple of t
                if n >= t and n % t == 0:
                    min_increment_for_t = 0  # No increment needed since n is already a multiple of t
                    break
                elif n < t:
                    # Calculate necessary increments for this n to be >= t and a multiple of t
                    next_multiple_of_t = (n // t + 1) * t
                    min_increment_for_t = min(min_increment_for_t, next_multiple_of_t - n)
            # Aggregate the increments needed for this target number
            increments += min_increment_for_t
        return increments