import pythoness
from typing import List, Optional

class Solution:
    
    def minCostGoodCaption(self, caption: str) -> str:
        """
        Convert a given string caption into a 'good caption' where each character appears in groups of at least 3 consecutive occurrences. Utilize operations to change any character to its adjacent in the alphabet, aiming for the minimum number of changes. Return the lexicographically smallest possible good caption or an empty string if conversion is impossible.
    
        Constraints:
        - 1 <= caption.length <= 5 * 10^4
        - The string consists only of lowercase English letters.
        """
        # Group the caption into sequences of identical characters
        from collections import defaultdict
        from heapq import heappop, heappush
        # Helper to find consecutive groups
        current_char = ''
        current_count = 0
        groups = []  # stores (character, count)
        for char in caption:
            if char == current_char:
                current_count += 1
            else:
                if current_char:
                    groups.append((current_char, current_count))
                current_char = char
                current_count = 1
        # Append final group
        if current_char:
            groups.append((current_char, current_count))
        # Priority queue to store cost changes
        # cost, pos, target_char
        pq = []
        # Process each group
        for (i, (char, count)) in enumerate(groups):
            if count >= 3:
                continue  # already a good group
            needed = 3 - count  # number of characters needed to form a group
            # Explore changing to same character
            # and also check lexicographical order by considering neighbours
            if i > 0 and groups[i - 1][0] != char:  # previous group, not same char
                prev_char = chr(ord(char) - 1)
                if groups[i - 1][0] == prev_char:
                    heappush(pq, (needed, i, prev_char))
            if i < len(groups) - 1 and groups[i + 1][0] != char:  # next group, not same char
                next_char = chr(ord(char) + 1)
                if groups[i + 1][0] == next_char:
                    heappush(pq, (needed, i, next_char))
        # Apply changes from the priority queue
        result = list(caption)
        while pq:
            (needed, idx, target_char) = heappop(pq)
            (char, count) = groups[idx]
            # Check if still need to change
            if count < 3:
                for j in range(len(result)):
                    if result[j] == char and needed > 0:
                        result[j] = target_char
                        needed -= 1
                groups[idx] = (target_char, groups[idx][1] + needed)  # update new count
        # Verify result
        final_groups = defaultdict(int)
        for char in result:
            final_groups[char] += 1
            if final_groups[char] == 3:
                final_groups.pop(char)  # reset once we fulfill a sequence
        return ''.join(result) if not final_groups else ''