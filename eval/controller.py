from __future__ import annotations

import util.setup as setup
import util.query as query

import glob
import os
import re
import shutil
import subprocess
import json
import random
from time import sleep

# Get from browser cookies
# SESSION = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTU2MjIxMDEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0YzU1ODI3MmI4MWYyMGI2MTI5MGRjM2M1ODdmNzllYzkxZWYyMWM2N2YzZDI4ODQzNDY1OWRiMDUwNDhmYjJjIiwic2Vzc2lvbl91dWlkIjoiMjEwZjA1NDMiLCJpZCI6MTU2MjIxMDEsImVtYWlsIjoia3lsYS5sZXZpbkBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImtobGV2aW4iLCJ1c2VyX3NsdWciOiJraGxldmluIiwiYXZhdGFyIjoiaHR0cHM6Ly9hc3NldHMubGVldGNvZGUuY29tL3VzZXJzL2tobGV2aW4vYXZhdGFyXzE3MzE3MjQzMjgucG5nIiwicmVmcmVzaGVkX2F0IjoxNzQxMzY0MTA4LCJpcCI6IjEyOC4xMTkuNDAuMTk2IiwiaWRlbnRpdHkiOiI2ZGJiMTA5NTJhMzhjMTFkMTllMjY0ODAyM2Q1MDU1YiIsImRldmljZV93aXRoX2lwIjpbImFiNGM0Mjg3NGYzMDQzNGEwYmNhM2MxY2UxNTNkNmMyIiwiMTI4LjExOS40MC4xOTYiXX0.tNOvbMpoyc525wO3U9b7PA4d3xcWoaBzC1ZdKrOOqY4"
# CSRF = "AgRlMyz6zKAphcqcgSNwf9JDtncqsAoLnCeYFYOYTfbh7WtQueK6lojOkjOaxIQU"


def _wrap_in_solution_class(code: str, func_name: str) -> str:
    lines = code.split("\n")
    import_lines = []
    non_import_lines = []
    in_import_section = True

    for line in lines:
        if in_import_section and re.match(r"^\s*(import|from\s+\S+\s+import)\s+", line):
            import_lines.append(line)
        else:
            in_import_section = False
            non_import_lines.append(line)

    # Indent the function and its body
    new_code = []
    for i, line in enumerate(non_import_lines):
        if re.match(rf"^\s*def {func_name}\s*\(", line):  # Function definition line
            # Insert "self" as the first argument if it's missing
            line = re.sub(rf"def {func_name}\(\s*", f"def {func_name}(self, ", line)
            new_code.append("    " + line)  # Indent function
        else:
            new_code.append("    " + line)  # Indent function body

    return "\n".join(import_lines) + "\n\nclass Solution:\n" + "\n".join(new_code)


def run_pythoness(list_problems: list, config: int, runs: int) -> None:
    ids = list_problems.keys()
    for id in ids:
        i = 0

        # Clear output contents if pre-existing
        if os.path.exists(f"./results/{id}/p{id}_config{config}.out"):
            open(f"./results/{id}/p{id}_config{config}.out", "w").close()

        while i < runs:
            i += 1
            print(
                f"Running iteration {i} of Pythoness on p{id}_config{config}_{i}.py..."
            )

            # Create file for output Python code, replacing it if necessary
            out_file = f"./results/{id}/p{id}_config{config}_{i}.py"
            if os.path.exists(out_file):
                os.remove(out_file)
            shutil.copy(f"./results/{id}/p{id}_config{config}.py", out_file)

            # Open the file for writing the output
            with open(f"./results/{id}/p{id}_config{config}.out", "a") as file:
                file.write(
                    f"\n\nRunning iteration {i} of Pythoness on p{id}_config{config}_{i}.py\n\n"
                )
                # Run the process and capture stdout
                process = subprocess.Popen(
                    [
                        "python3",
                        f"./results/{id}/p{id}_config{config}_{i}.py",
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )

                # Read and print the output line by line
                for line in process.stdout:
                    file.write(line)

                process.stdout.close()
                process.wait()

            with open(out_file, "r") as file:
                llm_code = file.read()

            # Check if Pythoness was successful, if not, skip
            if llm_code.find('""""""') != -1:
                print("Pythoness failed! Skipping.")
                continue
            else:
                print(f"Adding solution class to {os.path.basename(out_file)}...")
            # Get func_name
            func_name = setup.get_function_name(list_problems, id)

            # Strip Pythoness import, docstring, function call
            # llm_code = re.sub(r"import pythoness\n", "", llm_code)
            # llm_code = re.sub(r'"""(.*?)"""', "", llm_code, flags=re.DOTALL)
            llm_code = llm_code[: llm_code.rfind(func_name)].strip()

            # Wrap in Solution class (including imports)
            llm_code = _wrap_in_solution_class(llm_code, func_name)

            with open(f"{out_file}", "w") as file:
                file.write(llm_code)


def check_solution(list_problems: dict, config: int) -> dict:
    for id, name in list_problems.items():

        pattern = os.path.join(f"./results/{id}/", f"p{id}_config{config}_*.py")

        # Loop through all matching files
        for filepath in glob.glob(pattern):
            with open(filepath, "r") as file:
                llm_code = file.read()

            print(f"Checking {os.path.basename(filepath)}... ")

            # Check if Pythoness was successful, if not, skip
            if llm_code.find('""""""') != -1:
                print("Pythoness failed! Skipping.")
                continue

            # Strip Pythoness import, function call, docstring
            llm_code = re.sub(r"import pythoness\n", "", llm_code)
            llm_code = re.sub(r"from typing import List, Optional\n", "", llm_code)
            llm_code = "\n".join(llm_code.splitlines()[:-1])
            llm_code = re.sub(r'"""(.*?)"""', "", llm_code, flags=re.DOTALL)

            with open(f"{filepath[:-3]}_sol.txt", "w") as file:
                file.write(llm_code)

            # Only run specific files
            # if os.path.basename(filepath)[:-3] != "23_config1_1":
            #     continue

            # Get problem details, write to json
            print(f"Submitting {os.path.basename(filepath)}... ", end="")

            real_id = setup.get_id(list_problems, id)
            s_details = query.submit_solution(name, real_id, llm_code)
            print("Success!")
            with open(f"{filepath[:-3]}_sol.json", "w") as json_file:
                json.dump(s_details, json_file, indent=4)

            # Take a random break between POST requests - 4s min
            sleep(random.uniform(10, 15))

    return


def main():
    # list_problems = {
    #     # "4": "median-of-two-sorted-arrays",
    #     # "10": "regular-expression-matching",
    #     # "23": "merge-k-sorted-lists",  # 23 AND 25 DO NOT WORK. Given tests are "simplified" and not formatted correctly.
    #     # "25": "reverse-nodes-in-k-group",
    #     # "30": "substring-with-concatenation-of-all-words",
    #     # "32": "longest-valid-parentheses",
    #     # "41": "first-missing-positive",
    #     # "42": "trapping-rain-water",
    #     # "44": "wildcard-matching",
    #     # "493": "reverse-pairs",
    #     # "600": "non-negative-integers-without-consecutive-ones",
    #     # "668": "kth-smallest-number-in-multiplication-table",
    #     # "699": "falling-squares",
    #     # "765": "couples-holding-hands",
    #     # "801": "minimum-swaps-to-make-sequences-increasing",
    #     # "871": "minimum-number-of-refueling-stops",
    #     # "902": "numbers-at-most-n-given-digit-set",
    #     # "1416": "restore-the-array",  # No repo sol
    #     # "1923": "longest-common-subpath",
    #     # "2251": "number-of-flowers-in-full-bloom",
    #     # "2334": "subarray-with-elements-greater-than-varying-threshold",
    #     # "3312": "sorted-gcd-pair-queries",
    #     # "3410": "maximize-subarray-sum-after-removing-all-occurrences-of-one-element",
    #     # "3425": "longest-special-path",

    # }
    list_problems = {
        # "37": "sudoku-solver",
        # "51": "n-queens",
        # "466": "count-the-repetitions",
        # "552": "student-attendance-record-ii",
        # "850": "rectangle-area-ii",
        # "2872": "maximum-number-of-k-divisible-components",
        # "3197": "find-the-minimum-area-to-cover-all-ones-ii",
        # "3229": "separate-squares-ii",
        # "3448": "count-substrings-divisible-by-last-digit",
        # "3449": "maximize-the-minimum-game-score",
        # "3454": "separate-squares-ii",  # No repo sol
        # "3455": "shortest-matching-substring",
        "3459": "length-of-longest-v-shaped-diagonal-segment",
        # "3463": "check-if-digits-are-equal-in-string-after-operations-ii",
        # "3464": "maximize-the-distance-between-points-on-a-square",
        # "3470": "permutations-iv",
        # "3474": "lexicographically-smallest-generated-string",
        # ##################
        # "3405": "count-the-number-of-arrays-with-k-matching-adjacent-elements",
        # "3414": "maximum-score-of-non-overlapping-intervals",
        # "3420": "count-non-decreasing-subarrays-after-k-operations",
        # "3426": "manhattan-distances-of-all-arrangements-of-pieces",
        # "3430": "maximum-and-minimum-sums-of-at-most-size-k-subarrays",
        # "3435": "frequencies-of-shortest-supersequences",
        # "3441": "minimum-cost-good-caption",
        # "3444": "minimum-increments-for-target-multiples-in-an-array",
        # "3445": "maximum-difference-between-even-and-odd-frequency-ii",
    }

    configs = [2]

    # GET problem -> p[id]_problem.json
    # setup.get_problem(list_problems)

    for config in configs:
        pass
        # Generate config files -> p[id]_config#.py
        setup.generate_py_problems(list_problems, config)
        # # Run Pythoness -> p[id]_config#.out, p[id]_config#_#.py
        # run_pythoness(list_problems, config, 3)
        # Evaluate Results
        # check_solution(list_problems, config)


if __name__ == "__main__":
    main()
