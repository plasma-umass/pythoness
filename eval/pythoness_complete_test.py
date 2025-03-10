from __future__ import annotations

from time import sleep
from query import get_problem_details, submit_solution

import re
import subprocess

# Get from browser cookies
# SESSION = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTU2MjIxMDEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0YzU1ODI3MmI4MWYyMGI2MTI5MGRjM2M1ODdmNzllYzkxZWYyMWM2N2YzZDI4ODQzNDY1OWRiMDUwNDhmYjJjIiwic2Vzc2lvbl91dWlkIjoiMjEwZjA1NDMiLCJpZCI6MTU2MjIxMDEsImVtYWlsIjoia3lsYS5sZXZpbkBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImtobGV2aW4iLCJ1c2VyX3NsdWciOiJraGxldmluIiwiYXZhdGFyIjoiaHR0cHM6Ly9hc3NldHMubGVldGNvZGUuY29tL3VzZXJzL2tobGV2aW4vYXZhdGFyXzE3MzE3MjQzMjgucG5nIiwicmVmcmVzaGVkX2F0IjoxNzQxMzY0MTA4LCJpcCI6IjEyOC4xMTkuNDAuMTk2IiwiaWRlbnRpdHkiOiI2ZGJiMTA5NTJhMzhjMTFkMTllMjY0ODAyM2Q1MDU1YiIsImRldmljZV93aXRoX2lwIjpbImFiNGM0Mjg3NGYzMDQzNGEwYmNhM2MxY2UxNTNkNmMyIiwiMTI4LjExOS40MC4xOTYiXX0.tNOvbMpoyc525wO3U9b7PA4d3xcWoaBzC1ZdKrOOqY4"
# CSRF = "AgRlMyz6zKAphcqcgSNwf9JDtncqsAoLnCeYFYOYTfbh7WtQueK6lojOkjOaxIQU"


def extract_examples(text, func_name):
    pattern = re.compile(
        r"Example \d+:\s*" r"Input: (.*?)\s*" r"Output: (.*?)\s*" r"Explanation:",
        re.DOTALL,
    )

    matches = pattern.findall(text)
    results = []

    for inputs, output in matches:
        inputs = inputs.strip()
        output = output.strip()
        results.append(f"{func_name}({inputs}) == {output}")

    return results


def get_function_name(code):
    match = re.search(r"\bdef\s+(\w+)", code)
    if match:
        return match.group(1)
    else:
        return None


def leetcode_to_pythoness(list_problems, run_template):
    for id, name in list_problems.items():
        # Get prompt and template code
        # details = get_problem_details(name)
        details = {
            "difficulty": "Hard",
            "premium": "false",
            "problem_statement": "Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.\nThe overall run time complexity should be O(log (m+n)).\n\u00a0\nExample 1:\n\nInput: nums1 = [1,3], nums2 = [2]\nOutput: 2.00000\nExplanation: merged array = [1,2,3] and median is 2.\n\nExample 2:\n\nInput: nums1 = [1,2], nums2 = [3,4]\nOutput: 2.50000\nExplanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.\n\n\u00a0\nConstraints:\n\nnums1.length == m\nnums2.length == n\n0 <= m <= 1000\n0 <= n <= 1000\n1 <= m + n <= 2000\n-10^6 <= nums1[i], nums2[i] <= 10^6\n\n",
            "template_code_definition": "class Solution:\n    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:\n        pass",
        }
        if details["difficulty"] != "Hard" or details["premium"] != "false":
            print(
                f"Problem is either not Hard or not free. Difficulty: {details['difficulty']}, Premium: {details['premium']}",
            )
            return
        prompt = details["problem_statement"]
        template = details["template_code_definition"]

        # Overwrite test.py with template code
        with open(run_template, "r") as template_file:
            content = template_file.read()

        # Extract examples as unit tests
        func_name = get_function_name(template)
        unittests = ", ".join([f'"{i}"' for i in extract_examples(prompt, func_name)])
        prompt = re.sub(r"\nExample 1.*?(?=\nConstraints)", "", prompt, flags=re.DOTALL)
        content = re.sub(r"tests=\[\]", f"tests=[{unittests}]", content)

        # Insert prompt as func docstring
        index = content.find('"""')
        content = content[: index + 3] + prompt.strip() + content[index + 3 :]

        # Replace foo with func_name
        content = content.replace("Solution.foo()", f"Solution.{func_name}()").replace(
            "def foo(", f"def {func_name}("
        )

        # Find all O() mentions
        pattern = r"O\((?:[^()]*|(?:[^()]*\([^()]*\)))*\)"
        matches = re.findall(pattern, prompt)
        for match in matches:
            print(match)

        # Write full program to test.py
        with open("test.py", "w") as target_file:
            target_file.write(content)

        print(content)

        print("Running...")
        # result = subprocess.run(["python3", "test.py"], capture_output=True, text=True)

        # with open("modified_output.txt", "w") as f:
        #     f.write(result.stdout)

        # submit_solution(name, id)


def main():
    list_problems = {
        "4": "median-of-two-sorted-arrays",
        # "10": "regular-expression-matching",
        # "23": "merge-k-sorted-lists",
        # "25": "reverse-nodes-in-k-group",
        # "30": "substring-with-concatenation-of-all-words",
        # "32": "longest-valid-parentheses",
        # "37": "sudoku-solver",
        # "41": "first-missing-positive",
        # "42": "trapping-rain-water",
        # "44": "wildcard-matching",
    }

    run_template = "pythoness_template_1.txt"
    leetcode_to_pythoness(list_problems, run_template)


if __name__ == "__main__":
    main()
