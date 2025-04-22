
from p3463_config1_5 import Solution

inputs_list = [{'s': '111111111'}, {'s': '9876543210'}, {'s': '121212121212'}, {'s': '000000000000'}, {'s': '246813579'}, {'s': '808080808080'}, {'s': '112233445566778899'}, {'s': '01234567890123456789'}, {'s': '1029384756'}, {'s': '5678901234567890'}]

for i in range(len(inputs_list)):
    try:
        print(Solution().hasSameDigits(**inputs_list[i]))
    except Exception as e:
        print("Input failed: ", inputs_list[i], "    Error: ", e)
