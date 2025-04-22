
from p3445_config1_5 import Solution

inputs_list = [{'s': '000111222333444000', 'k': 5}, {'s': '1010101010101010', 'k': 2}, {'s': '432104321', 'k': 1}, {'s': '333444', 'k': 3}, {'s': '444333222111000', 'k': 6}, {'s': '11111122223333', 'k': 8}, {'s': '0123443210000', 'k': 5}, {'s': '142323142', 'k': 1}, {'s': '4444444444444444', 'k': 15}, {'s': '031204320315', 'k': 11}]

for i in range(len(inputs_list)):
    try:
        print(Solution().maxDifference(**inputs_list[i]))
    except Exception as e:
        print("Input failed: ", inputs_list[i], "    Error: ", e)
