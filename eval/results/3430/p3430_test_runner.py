
from p3430_config3_3 import Solution

inputs_list = [{'nums': [5, 5, 5, 5, 5], 'k': 5}, {'nums': [-1, -2, -3, -4, -5], 'k': 2}, {'nums': [1, 3, 2, 5, 4, 8, 6, 7, 9], 'k': 5}, {'nums': [1, 2], 'k': 2}, {'nums': [-5, -1, -3, -4, 0, 2, 1, 3, 4], 'k': 9}, {'nums': [10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 'k': 6}, {'nums': [0], 'k': 1}, {'nums': [100000, 200000, 300000, 400000, 500000], 'k': 4}, {'nums': [-3, -1, -4, -2, -5], 'k': 2}, {'nums': [123456, 654321, 1000000, -1000000, -999999], 'k': 4}]

for i in range(len(inputs_list)):
    try:
        print(Solution().minMaxSubarraySum(**inputs_list[i]))
    except Exception as e:
        print("Input failed: ", inputs_list[i], "    Error: ", e)
