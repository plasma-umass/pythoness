import pythoness
from typing import List, Optional

class Solution:
    
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        """
        Calculates the minimum number of operations needed to ensure each element in the target array has at least one multiple in the nums array. In each operation, any element in nums can be incremented by 1. The function ensures compliance with constraints on array lengths and element values.
        """
    
        def has_multiple(element, nums):
            # Check if any number in nums is a multiple of the element
            for number in nums:
                if number % element == 0:
                    return True
            return False
        min_increments = 0
        for t in target:
            if not has_multiple(t, nums):
                # Find the minimum increment needed to make one of the nums divisible by t
                best_increment = float('inf')
                for num in nums:
                    increment = (t - num % t) % t
                    best_increment = min(best_increment, increment)
                min_increments += best_increment
                if best_increment > 0:
                    # Apply the best increment to one of the num in nums
                    for (i, num) in enumerate(nums):
                        if (num + best_increment) % t == 0:
                            nums[i] = num + best_increment
                            break
        return str(min_increments)