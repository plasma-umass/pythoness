
from p3455_config1_2 import Solution

inputs_list = [{'s': 'abcde', 'p': 'a*e*'}, {'s': 'mississippi', 'p': 'm*s*i'}, {'s': 'abcdefghijklmnopqrstuvwxyz', 'p': 'a*z*'}, {'s': 'banana', 'p': 'b*n*n'}, {'s': 'fluffyfluffles', 'p': '*u*yf'}, {'s': 'thequickbrownfox', 'p': 't*q*ox'}, {'s': 'ggggrrrr', 'p': 'g*r*'}, {'s': 'abababa', 'p': 'b*b*'}, {'s': 'abcdefghijklmnop', 'p': 'a*p*n'}, {'s': 'squidwardtentacles', 'p': 's*u*s'}]

for i in range(len(inputs_list)):
    try:
        print(Solution().shortestMatchingSubstring(**inputs_list[i]))
    except Exception as e:
        print("Input failed: ", inputs_list[i], "    Error: ", e)
