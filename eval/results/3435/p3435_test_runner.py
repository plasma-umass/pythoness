
from p3435oracle import Solution

inputs_list = [{'words': ['ab', 'bc', 'ca']}, {'words': ['ax', 'xb', 'ay', 'by']}, {'words': ['ab', 'cd', 'ef', 'gh']}, {'words': ['mq', 'qn', 'nm', 'mp']}, {'words': ['za', 'az']}, {'words': ['xy', 'yx', 'xx', 'yy']}, {'words': ['ab', 'bc']}, {'words': ['po', 'op', 'pp']}, {'words': ['fg', 'gf']}, {'words': ['lm', 'mn', 'no']}, {'words': ['ba', 'bb', 'bc']}, {'words': ['aa', 'bb', 'cc']}, {'words': ['rs', 'st']}, {'words': ['zz', 'zx', 'xz']}, {'words': ['ik', 'kj', 'ji', 'if']}, {'words': ['qa', 'aq', 'pq']}, {'words': ['wv', 'vw', 'vv']}, {'words': ['gg', 'gh', 'hg']}, {'words': ['ek', 'ke']}, {'words': ['vw', 'wx', 'xy', 'yu']}]

for i in range(len(inputs_list)):
    try:
        print(Solution().supersequences(**inputs_list[i]))
    except Exception as e:
        print("Input failed: ", inputs_list[i], "    Error: ", e)
