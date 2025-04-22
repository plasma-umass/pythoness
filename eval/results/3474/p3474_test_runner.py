
from p3474_config3_2 import Solution

inputs_list = [{'str1': 'TTFFT', 'str2': 'abc'}, {'str1': 'TFTFTF', 'str2': 'xyz'}, {'str1': 'FTTTTTF', 'str2': 'opqrs'}, {'str1': 'TF', 'str2': 'longsubstring'}, {'str1': 'TFTF', 'str2': 'abc'}, {'str1': 'FFFF', 'str2': 'cat'}, {'str1': 'FTFTFTTFT', 'str2': 'hello'}, {'str1': 'T', 'str2': 'a'}, {'str1': 'FFFTFF', 'str2': 'xyz'}, {'str1': 'FTFTFT', 'str2': 'bc'}]

for i in range(len(inputs_list)):
    try:
        print(Solution().generateString(**inputs_list[i]))
    except Exception as e:
        print("Input failed: ", inputs_list[i], "    Error: ", e)
