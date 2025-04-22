
from p3444_config2_1 import Solution

inputs_list = [{'nums': [15, 25, 35, 45, 55], 'target': [3, 4]}, {'nums': [50, 60, 70, 80, 90, 100], 'target': [8]}, {'nums': [1, 1, 1, 1, 1], 'target': [2, 3, 4]}, {'nums': [2, 2, 2, 2, 2], 'target': [7]}, {'nums': [10000, 9999, 9998], 'target': [5000]}, {'nums': [9, 18, 27, 36, 45], 'target': [3, 13]}, {'nums': [100, 200, 300, 400], 'target': [33, 44, 55, 66]}, {'nums': [1, 3, 5, 7, 9, 11, 13, 15], 'target': [2]}, {'nums': [18, 36, 54, 72], 'target': [7, 9]}, {'nums': [500, 500, 500, 500, 500], 'target': [1, 2, 3, 4]}]

for i in range(len(inputs_list)):
    try:
        print(Solution().minimumIncrements(**inputs_list[i]))
    except Exception as e:
        print("Input failed: ", inputs_list[i], "    Error: ", e)
