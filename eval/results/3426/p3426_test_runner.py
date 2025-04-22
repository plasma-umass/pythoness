
from p3426_config1_2 import Solution

inputs_list = [{'m': 1, 'n': 2, 'k': 2}, {'m': 250, 'n': 400, 'k': 500}, {'m': 50, 'n': 50, 'k': 1250}, {'m': 817, 'n': 122, 'k': 2000}, {'m': 2, 'n': 2, 'k': 2}, {'m': 123, 'n': 456, 'k': 15000}, {'m': 5000, 'n': 20, 'k': 10000}, {'m': 700, 'n': 1400, 'k': 2800}, {'m': 450, 'n': 450, 'k': 50000}, {'m': 1, 'n': 50000, 'k': 10}]

for i in range(len(inputs_list)):
    try:
        print(Solution().distanceSum(**inputs_list[i]))
    except Exception as e:
        print("Input failed: ", inputs_list[i], "    Error: ", e)
