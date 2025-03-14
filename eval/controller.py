from __future__ import annotations

from time import sleep
from query import get_problem_details

import glob
import json
import os
import re
import shutil
import subprocess


def extract_examples(text, func_name):
    pattern = r"Input:\s*(.*?)\nOutput:\s*(.*?)\n(?:Explanation|Example|Constraints)"
    matches = re.findall(pattern, text, re.DOTALL)

    # Find all matches in the input string
    results = []
    for inputs, output in matches:
        inputs = "".join(line.strip() for line in inputs.splitlines())
        output = "".join(line.strip() for line in output.splitlines())

        inputs = inputs.strip().replace("false", "False").replace("true", "True")
        output = output.strip().replace("false", "False").replace("true", "True")
        results.append(f"{func_name}({inputs}) == {output}")

    return results


def get_function_name(code):
    matches = re.findall(r"\bdef\s+(\w+)", code)  # Finds all function names
    if matches:
        return matches[-1]  # Returns the last function name
    else:
        return None  # Returns None if no match is found


def remove_imports(code):
    # Split the multiline string into lines
    lines = code.splitlines()

    # List to store the resulting lines after removing the imports
    result_lines = []

    # Flag to determine if we've reached the function definition
    reached_def = False

    # Loop through each line
    for line in lines:
        if reached_def:
            result_lines.append(line)  # Add all lines after reaching 'def'
        elif line.strip().startswith(("from", "import")):
            continue  # Skip the lines starting with 'from' or 'import'
        elif line.strip().startswith("def "):
            reached_def = (
                True  # Stop skipping lines once we reach a function definition
            )
            result_lines.append(line)  # Add the function definition itself

    # Join the remaining lines back into a single string
    return "\n".join(result_lines)


def wrap_in_solution_class(code: str, func_name) -> str:
    lines = code.split("\n")
    new_code = []

    for i, line in enumerate(lines):
        if re.match(rf"^\s*def {func_name}\s*\(", line):  # Function definition line
            # Insert "self" as the first argument if it's missing
            line = re.sub(rf"def {func_name}\(\s*", f"def {func_name}(self, ", line)
            new_code.append("    " + line)  # Indent function
        else:
            new_code.append("    " + line)  # Indent function body

    return "class Solution:\n" + "\n".join(new_code)


def generate_json_problem(list_problems: dict, id) -> dict:
    if isinstance(list_problems[id], tuple):
        name = list_problems[id][0]
    else:
        name = list_problems[id]

    # Get problem details, write to json
    details = get_problem_details(name)

    if not os.path.exists(f"./results/{id}"):
        os.makedirs(f"./results/{id}")

    with open(f"./results/{id}/{id}_problem.json", "w") as json_file:
        json.dump(details, json_file, indent=4)

    # Take a break between GET requests
    sleep(5)

    return details


def generate_py_problem(list_problems: dict, config: int) -> str:
    i = 0
    tot = len(list_problems)
    for id, name in list_problems.items():
        i += 1

        print(f"Creating {id} {name}.py... {i}/{tot}")

        if not os.path.exists(f"./results/{id}"):
            os.makedirs(f"./results/{id}")

        # Retrieve prompt and template code
        if os.path.exists(f"./results/{id}/{id}_problem.json"):
            with open(f"./results/{id}/{id}_problem.json", "r") as file:
                details = json.load(file)
        else:
            details = generate_json_problem(list_problems, id)

        if "difficulty" not in details or "premium" not in details:
            print("Problem details not found")
            print(details.keys())
            return

        if details["difficulty"] != "Hard" or details["premium"]:
            print(
                f"Problem is either not Hard or not free. Difficulty: {details['difficulty']}, Premium: {details['premium']}",
            )
            return
        prompt = details["problem_statement"].replace("\xa0", "")
        template = details["template_code_snippet"]

        if config == 1:
            template_insert = "\n    llm_unit=False,\n    llm_prop=False,"
        elif config == 2:
            template_insert = "\n    llm_prop=False,"
        elif config == 4:
            template_insert = "\n    runtime=True,"
        else:
            template_insert = ""

        # Overwrite test.py with template code and insert chosen config
        with open("pythoness_template.txt", "r") as template_file:
            content = template_file.read()

        content = content.replace("tests=[],", "tests=[]," + template_insert)

        for line in template.splitlines():
            if line.lstrip().startswith(
                "def "
            ):  # Stripping leading spaces to allow for indentation
                f_def = line.strip()
        content = (
            content.replace("def dummy_func():", f_def)
            .replace("self, ", "")
            .replace("self", "")
        )

        # Extract examples as unit tests
        func_name = get_function_name(template)
        unittests = extract_examples(prompt, func_name)
        # print(unittests)
        all_unittests = ", ".join([f"'{i}'" for i in unittests])
        # print(all_unittests)

        prompt = re.sub(r"\nExample 1.*?(?=\nConstraints)", "", prompt, flags=re.DOTALL)
        content = re.sub(r"tests=\[\]", f"tests=[{all_unittests}]", content)

        # Remove any Follow-up section
        index = prompt.find("\nFollow-up:")
        prompt = prompt[:index].strip() if index != -1 else prompt

        # Insert prompt as func docstring
        index = content.find('"""')
        content = content[: index + 3] + prompt.strip() + content[index + 3 :]

        # Replace call to foo
        content = content.replace(
            "dummy_func()", unittests[0][: unittests[0].find("==")]
        )

        # Find all O() mentions
        pattern = r"O\((?:[^()]*|(?:[^()]*\([^()]*\)))*\)"
        matches = re.findall(pattern, prompt)
        if len(matches) > 0:
            if len(matches) == 1:
                print("One runtime bound match")
                content = content.replace(
                    "time_bound=None,",
                    f'time_bound="{matches[0]}",\n    range=(),',
                )
            else:
                print("Multiple runtime bound match")

        # Write full program to id_config#.py
        with open(f"./results/{id}/{id}_config{config}.py", "w") as target_file:
            target_file.write(content)


def run_pythoness(ids: list, config: int, runs: int) -> None:
    for id in ids:
        i = 0

        # Clear output contents if pre-existing
        if os.path.exists(f"./results/{id}/{id}_config{config}.out"):
            open(f"./results/{id}/{id}_config{config}.out", "w").close()

        while i < runs:
            i += 1
            print(
                f"Running iteration {i} of Pythoness on {id}_config{config}_{i}.py..."
            )

            # Create file for output Python code, replacing it if necessary
            out_file = f"./results/{id}/{id}_config{config}_{i}.py"
            if os.path.exists(out_file):
                os.remove(out_file)
            shutil.copy(f"./results/{id}/{id}_config{config}.py", out_file)

            # Open the file for writing the output
            with open(f"./results/{id}/{id}_config{config}.out", "a") as file:
                file.write(
                    f"\n\nRunning iteration {i} of Pythoness on {id}_config{config}_{i}.py\n\n"
                )
                # Run the process and capture stdout
                process = subprocess.Popen(
                    [
                        "python3",
                        f"./results/{id}/{id}_config{config}_{i}.py",
                    ],  # Replace with your command
                    stdout=subprocess.PIPE,  # Capture stdout
                    stderr=subprocess.PIPE,  # Capture stderr if needed
                    text=True,  # Ensure output is in text format (not bytes)
                )

                # Read and print the output line by line
                for line in process.stdout:
                    # print(line, end="")  # Print to terminal
                    file.write(line)  # Write to the file

                # Wait for the process to finish
                process.stdout.close()
                process.wait()


def make_solution(list_problems: dict, config: int) -> dict:
    for id, name in list_problems.items():

        pattern = os.path.join(f"./results/{id}/", f"{id}_config{config}_*.py")

        # Loop through all matching files
        for filepath in glob.glob(pattern):

            with open(filepath, "r") as file:
                llm_code = file.read()

            # Only run specific files
            if os.path.basename(filepath)[:-3] != "3459_config1_1":
                continue

            # Check if Pythoness was successful, if not, skip
            if llm_code.find('""""""') != -1:
                print("Pythoness failed! Skipping.")
                continue

            # Strip Pythoness import, function call, docstring
            llm_code = re.sub(r"import pythoness\n", "", llm_code)
            llm_code = re.sub(r"from typing import List, Optional\n", "", llm_code)
            # llm_code = "\n".join(llm_code.splitlines()[:-1])
            llm_code = re.sub(r'"""(.*?)"""', "", llm_code, flags=re.DOTALL)

            # Wrap in Solution class (including imports)
            if os.path.exists(f"./results/{id}/{id}_problem.json"):
                with open(f"./results/{id}/{id}_problem.json", "r") as file:
                    details = json.load(file)
            else:
                details = generate_json_problem(list_problems, id)
            func_name = get_function_name(details["template_code_definition"])

            llm_code = wrap_in_solution_class(llm_code, func_name)

            print(f"Writing to {os.path.basename(filepath)[:-3]}.txt...")
            with open(f"{filepath[:-3]}.txt", "w") as file:
                file.write(llm_code)

    return


def main():
    list_problems = {
        # "4": "median-of-two-sorted-arrays",
        # "10": "regular-expression-matching",
        # "23": "merge-k-sorted-lists",  # 23 AND 25 DO NOT WORK. Given tests are "simplified" and not formatted correctly.
        # "25": "reverse-nodes-in-k-group",
        # "30": "substring-with-concatenation-of-all-words",
        # "32": "longest-valid-parentheses",
        # "41": "first-missing-positive",
        # "42": "trapping-rain-water",
        # "44": "wildcard-matching",
        # ##################
        # "493": "reverse-pairs",
        # "600": "non-negative-integers-without-consecutive-ones",
        # "668": "kth-smallest-number-in-multiplication-table",
        # "699": "falling-squares",
        # "765": "couples-holding-hands",
        # "801": "minimum-swaps-to-make-sequences-increasing",
        # ##################
        # "871": "minimum-number-of-refueling-stops",
        # "902": "numbers-at-most-n-given-digit-set",
        # "1416": "restore-the-array",  # No repo sol
        # "1923": "longest-common-subpath",
        # "2251": "number-of-flowers-in-full-bloom",
        # "2334": "subarray-with-elements-greater-than-varying-threshold",
        # "3312": "sorted-gcd-pair-queries",
        # ##################
        # "3445": "maximum-difference-between-even-and-odd-frequency-ii",
        # "3454": "separate-squares-ii",  # No repo sol
        # "3463": "check-if-digits-are-equal-in-string-after-operations-ii",
        # "3464": "maximize-the-distance-between-points-on-a-square",
        # "3470": "permutations-iv",
    }
    list_problems = {
        "37": "sudoku-solver",
        "51": "n-queens",
        "466": "count-the-repetitions",
        "552": "student-attendance-record-ii",
        "850": "rectangle-area-ii",
        "2872": "maximum-number-of-k-divisible-components",
        "3197": "length-of-longest-v-shaped-diagonal-segment",
        "3229": "separate-squares-ii",
        "3448": "count-substrings-divisible-by-last-digit",
        "3449": "maximize-the-minimum-game-score",
        "3455": "shortest-matching-substring",
        "3459": "length-of-longest-v-shaped-diagonal-segment",
        "3474": "lexicographically-smallest-generated-string",
    }

    config = 4
    # GET problem -> id_problem.json, id_config#.py
    generate_py_problem(list_problems, config)
    # Run Pythoness -> id_config#.out, id_config#_#.py
    # run_pythoness(list_problems.keys(), config, 5)
    # make_solution(list_problems, config)  # -> id_config#.txt


if __name__ == "__main__":
    main()
