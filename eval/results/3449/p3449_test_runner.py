
from p3449_config1_4 import Solution

inputs_list = [{'points': [1000000, 999999, 1000000], 'm': 1000000000}, {'points': [5, 3, 2, 1, 4], 'm': 10}, {'points': [10, 20, 30, 40, 50], 'm': 3}, {'points': [1, 1, 1, 1, 1], 'm': 20}, {'points': [1000], 'm': 100}, {'points': [10, 100, 10], 'm': 1}, {'points': [2, 2, 2, 2, 2, 2], 'm': 9}, {'points': [100, 200, 300, 400, 500], 'm': 6}, {'points': [1, 2, 3], 'm': 1}, {'points': [3, 3, 3, 3, 3, 3], 'm': 18}]

for i in range(len(inputs_list)):
    try:
        print(Solution().maxScore(**inputs_list[i]))
    except Exception as e:
        print("Input failed: ", inputs_list[i], "    Error: ", e)
