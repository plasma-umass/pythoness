
from p3441_config1_3 import Solution

inputs_list = [{'caption': 'ababab'}, {'caption': 'aaabbbccc'}, {'caption': 'ooo'}, {'caption': 'helloworld'}, {'caption': 'cccdddeeeff'}, {'caption': 'pppppp'}, {'caption': 'gghhiij'}, {'caption': 'zzzzzz'}, {'caption': 'abccba'}, {'caption': 'nnmmoolkkjj'}]

for i in range(len(inputs_list)):
    try:
        print(Solution().minCostGoodCaption(**inputs_list[i]))
    except Exception as e:
        print("Input failed: ", inputs_list[i], "    Error: ", e)
