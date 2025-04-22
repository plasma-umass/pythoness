from p3470_config1_5 import Solution

inputs_list = [
    {"n": 3, "k": 1},
    {"n": 6, "k": 15},
    {"n": 2, "k": 1},
    {"n": 9, "k": 50},
    {"n": 10, "k": 100},
    {"n": 3, "k": 3},
    {"n": 15, "k": 1000},
    {"n": 1, "k": 1},
    {"n": 11, "k": 100},
    {"n": 100, "k": 1000000000000},
]

for i in range(len(inputs_list)):
    try:
        print(Solution().permute(**inputs_list[i]))
    except Exception as e:
        print("Input failed: ", inputs_list[i], "    Error: ", e)
