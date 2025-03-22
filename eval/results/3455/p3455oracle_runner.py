
from p3455oracle import Solution

inputs_list = [{'s': 'abcde', 'p': 'a*c*e'}, {'s': 'ababababab', 'p': 'a*b*a'}, {'s': 'ccccccccccc', 'p': 'c*c*c'}, {'s': 'abxyzcd', 'p': 'a*xyz*d'}, {'s': 'qwertyuiop', 'p': 'qw*ui*p'}, {'s': 'longstringsample', 'p': 'long*str*ample'}, {'s': 'lllllmmmmm', 'p': 'l*m*m'}, {'s': 'abcsdfabc', 'p': 'a*df*c'}, {'s': 'mississippi', 'p': 'miss*issi*pi'}, {'s': 'randomstringwithastaring', 'p': 'rand*with*a'}, {'s': 'hellohithere', 'p': 'he*hi*re'}, {'s': 'short', 'p': 's*o*t'}, {'s': 'nothing', 'p': 'noth*hi*ing'}, {'s': 'prefixsuffix', 'p': 'pre*ix*suf'}, {'s': 'abcdefg', 'p': 'abc*e*f'}, {'s': 'abcdefghijklmnop', 'p': 'def*ghi*lmn'}, {'s': 'xyz', 'p': 'x*y*z'}, {'s': 'repeatpatterns', 'p': 'rep*pat*rns'}, {'s': '', 'p': '*a*b'}, {'s': 'findingnemo', 'p': 'fin*em*mo'}]

for i in range(len(inputs_list)):
    try:
        print(Solution().shortestMatchingSubstring(**inputs_list[i]))
    except Exception as e:
        print("Input failed: ", inputs_list[i], "    Error: ", e)
