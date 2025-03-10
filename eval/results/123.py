import pythoness
from typing import List

@pythoness.spec(
    """You are given an array prices where prices[i] is the price of a given stock on the i^th day.
Find the maximum profit you can achieve. You may complete at most two transactions.
Note: You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).
 
Constraints:

1 <= prices.length <= 10^5
0 <= prices[i] <= 10^5""",
    tests=['maxProfit(prices = [3,3,5,0,0,3,1,4]) == 6', 'maxProfit(prices = [1,2,3,4,5]) == 4', 'maxProfit(prices = [7,6,4,3,1]) == 0'],
    llm_unit=False,
    llm_prop=False,
    regenerate=True,
    verbose=True,
    output=True,
    time_bound=None,
)
def maxProfit(prices: List[int]) -> int:
    """"""

maxProfit()