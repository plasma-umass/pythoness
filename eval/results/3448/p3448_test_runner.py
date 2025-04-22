
from p3449_config1_1 import Solution

inputs_list = [{'s': '1000000000'}, {'s': '0000000001'}, {'s': '9876543210'}, {'s': '222222222'}, {'s': '1010101010'}, {'s': '1111111111111111111111111'}, {'s': '1'}, {'s': '0000000000000'}, {'s': '1000000000001'}, {'s': '999099909990999'}]

for i in range(len(inputs_list)):
    try:
        print(Solution().countSubstrings(**inputs_list[i]))
    except Exception as e:
        print("Input failed: ", inputs_list[i], "    Error: ", e)
