from __future__ import annotations

from setup import generate_py_problem, get_function_name, generate_json_problem
import assistant

import glob
import json
import os
import re
import shutil
import subprocess


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


def wrap_in_solution_class(code: str, func_name: str) -> str:
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


def run_pythoness(ids: list, config: int, runs: int) -> None:
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
                    stdout=subprocess.PIPE,  # Capture stdout
                    stderr=subprocess.PIPE,  # Capture stderr
                    text=True,
                )

                # Read and print the output line by line
                for line in process.stdout:
                    # print(line, end="")  # Print to terminal
                    file.write(line)

                process.stdout.close()
                process.wait()


def make_solution(list_problems: dict, config: int) -> dict:
    for id in list_problems.keys():

        pattern = os.path.join(f"./results/{id}/", f"p{id}_config{config}_*.py")
        all_files = [f for f in glob.glob(pattern) if not f.endswith("_pytest.py")]

        # Loop through all matching files
        for filepath in all_files:

            with open(filepath, "r") as file:
                llm_code = file.read()

            # Only run specific files
            # if os.path.basename(filepath)[:-3] != "3459_config1_1":
            #     continue

            # Check if Pythoness was successful, if not, skip
            if llm_code.find('""""""') != -1:
                print("Pythoness failed! Skipping.")
                continue

            # Get func_name
            if os.path.exists(f"./results/{id}/p{id}_problem.json"):
                with open(f"./results/{id}/p{id}_problem.json", "r") as file:
                    details = json.load(file)
            else:
                details = generate_json_problem(list_problems, id)
            func_name = get_function_name(details["template_code_definition"])

            # Strip Pythoness import, docstring, function call
            # llm_code = re.sub(r"import pythoness\n", "", llm_code)
            # llm_code = re.sub(r'"""(.*?)"""', "", llm_code, flags=re.DOTALL)
            llm_code = llm_code[: llm_code.rfind(func_name)].strip()

            # Wrap in Solution class (including imports)
            llm_code = wrap_in_solution_class(llm_code, func_name)

            print(f"Writing to {os.path.basename(filepath)[:-3]}_pytest.py...")
            with open(f"{filepath[:-3]}_pytest.py", "w") as file:
                file.write(llm_code)

    return


def setup_pytest_and_evaluate(config: int, specific_subdirs=None):
    parent_dir = "results"
    # Get full paths of all subdirectories
    all_subdirs = [
        d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))
    ]

    # If no specific subdirectories are provided, loop over all
    subdirs = specific_subdirs if specific_subdirs is not None else all_subdirs
    for subdir in subdirs:

        subdir_path = os.path.join("results", subdir)

        # Ensure destination directory exists
        os.makedirs(subdir_path, exist_ok=True)
        coverup_tests_pattern = f"{subdir_path}/tests/test_coverup_*.py"
        coverup_test_files = []

        # Make a copy of all coverup files
        for file_path in glob.glob(coverup_tests_pattern):
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(subdir_path, file_name)
            shutil.copy(file_path, destination_path)
            print(f"Copied {file_path} to {destination_path}")
            coverup_test_files.append(destination_path)

        # Iterate over all runs of this config
        file_pattern = f"p{subdir}_config{config}_*_pytest.py"
        pytests_pattern = os.path.join(subdir_path, file_pattern)
        pytests = glob.glob(pytests_pattern)

        # Clear output contents if pre-existing
        eval_output_file = f"./results/{subdir}/p{subdir}_config{config}_eval.out"
        if os.path.exists(eval_output_file):
            open(eval_output_file, "w").close()

        # pytests = ["./results/552/p552_config1_1_pytest.py"]

        for py in pytests:

            for file_to_modify in coverup_test_files:
                print("Modifying file:", file_to_modify)
                with open(file_to_modify, "r") as f:
                    lines = f.readlines()

                # Loop through lines to find the first one starting with "import src"
                for i, line in enumerate(lines):
                    # print(f"from src.p{subdir}oracle")
                    # print(line)
                    if line.startswith(f"from src.p{subdir}oracle") or line.startswith(
                        f"from p{subdir}_config{config}_"
                    ):
                        # print("Replacing...")
                        lines[i] = f"from {os.path.basename(py)[:-3]} import Solution\n"
                        break

                # Write the modified content back to the file
                with open(file_to_modify, "w") as f:
                    f.writelines(lines)

                print(f"Evaluating {py}...")
                with open(
                    f"./results/{subdir}/p{subdir}_config{config}_eval.out", "a"
                ) as file:
                    file.write(
                        f"\n\nEvaluating Pythoness result {py} on {file_to_modify}\n\n"
                    )
                    result = subprocess.run(
                        ["pytest", file_to_modify],
                        capture_output=True,
                        text=True,
                    )
                    file.write(result.stdout)
                    file.write(result.stderr)


def _query_inputs(prompt, subdir, test_file_path):
    print(f"Prompting GPT for unit tests for {subdir}...")
    client = assistant.Assistant()

    result = client.query(prompt)

    # Get inputs list and write to tests.json file
    try:
        inputs_list = json.loads(result)["inputs"]

        data = {"inputs": inputs_list}
        with open(test_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print("Error parsing JSON:", e)
        with open(test_file_path, "w") as json_file:
            json_file.write("")


def generate_unit_tests(list_problems):
    specific_subdirs = list_problems.keys()
    for subdir in specific_subdirs:
        subdir_path = os.path.join("results", subdir)
        test_file = f"p{subdir}_tests.json"
        test_file_path = os.path.join(subdir_path, test_file)

        # Get func_name
        if os.path.exists(f"./results/{subdir}/p{subdir}_problem.json"):
            with open(f"./results/{subdir}/p{subdir}_problem.json", "r") as file:
                details = json.load(file)
        else:
            details = generate_json_problem(list_problems, subdir)
        func_name = get_function_name(details["template_code_definition"])

        with open(os.path.join(subdir_path, f"p{subdir}_prompt_full.txt"), "r") as f:
            docstring = f.read().strip()

        with open(os.path.join(subdir_path, f"p{subdir}oracle.py"), "r") as f:
            func = f.read()

        for line in func.splitlines():
            if line.lstrip().startswith("def "):
                func = line.strip() + f'\n    """{docstring}"""'
                break

        # Ask GPT for validation set
        prompt = (
            f"""Generate 20 diverse inputs to fuzz-test the following function signature and description:\n\n```\n"""
            + func
            + "\n```\n"
            + """Return the result as a JSON object with the following structure:
```
{  
  "inputs": [  
    {"arg_name": value1, "arg_name": value2, ...},  
    {"arg_name": value3, "arg_name": value4, ...},  
    ... (20 entries)  
  ]  
}
```"""
        )

        # print(prompt)

        # _query_inputs(prompt, subdir, test_file_path)

        with open(test_file_path, "r") as file:
            inputs_list = json.load(file)["inputs"]

        print("Running oracle and collecting unit tests...")
        # Run ground truth and collect results
        runner = os.path.join(subdir_path, f"p{subdir}oracle_runner.py")
        with open(runner, "w") as f:
            f.write(
                f"""
from p{subdir}oracle import Solution

inputs_list = {inputs_list}

for i in range(len(inputs_list)):
    try:
        print(Solution().shortestMatchingSubstring(**inputs_list[i]))
    except Exception as e:
        print("Input failed: ", inputs_list[i], "    Error: ", e)
"""
            )

        result = subprocess.run(
            ["python3", runner],
            capture_output=True,
            text=True,
        )

        data = {"inputs": inputs_list, "outputs": result.stdout.splitlines()}

        # Write the result to the test file
        print("Writing to file:", test_file)
        try:
            with open(test_file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)
        except Exception as e:
            print("Error writing to file:", e)


def evaluate_results(specific_subdirs, config):

    for subdir in specific_subdirs:

        subdir_path = os.path.join("results", subdir)

        # Ensure destination directory exists
        os.makedirs(subdir_path, exist_ok=True)
        test_file = os.path.join(subdir_path, f"p{subdir}_tests.py")

        if os.path.exists(test_file):

            # Iterate over all runs of this config
            file_pattern = f"p{subdir}_config{config}_*_pytest.py"
            pytests_pattern = os.path.join(subdir_path, file_pattern)
            pytests = glob.glob(pytests_pattern)

            # Clear output contents if pre-existing
            eval_output_file = f"./results/{subdir}/p{subdir}_config{config}_eval.out"
            if os.path.exists(eval_output_file):
                open(eval_output_file, "w").close()

            # pytests = ["./results/552/p552_config1_1_pytest.py"]

            for py in pytests:

                print("Modifying file:", test_file)
                with open(test_file, "r") as f:
                    lines = f.readlines()

                # Loop through lines to find the first one starting with "import src"
                for i, line in enumerate(lines):
                    # print(f"from src.p{subdir}oracle")
                    # print(line)
                    if line.startswith(f"from src.p{subdir}oracle") or line.startswith(
                        f"from p{subdir}_config{config}_"
                    ):
                        # print("Replacing...")
                        lines[i] = f"from {os.path.basename(py)[:-3]} import Solution\n"
                        break

                # Write the modified content back to the file
                with open(test_file, "w") as f:
                    f.writelines(lines)

                print(f"Evaluating {py}...")
                with open(
                    f"./results/{subdir}/p{subdir}_config{config}_eval.out", "a"
                ) as file:
                    file.write(
                        f"\n\nEvaluating Pythoness result {py} on {test_file}\n\n"
                    )
                    result = subprocess.run(
                        ["pytest", test_file],
                        capture_output=True,
                        text=True,
                    )
                    file.write(result.stdout)
                    file.write(result.stderr)
        else:
            print(f"Tests file not found in {subdir}.")


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
    #     # ##################
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
    #     # ##################
    #     # "2334": "subarray-with-elements-greater-than-varying-threshold",
    #     # "3312": "sorted-gcd-pair-queries",
    #     # "3445": "maximum-difference-between-even-and-odd-frequency-ii",
    #     # ##################
    #     # "3410": "maximize-subarray-sum-after-removing-all-occurrences-of-one-element",
    #     # "3425": "longest-special-path",
    #     # "3430": "maximum-and-minimum-sums-of-at-most-size-k-subarrays",
    #     # "3435": "frequencies-of-shortest-supersequences",
    #     # "3444": "minimum-increments-for-target-multiples-in-an-array",
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
        "3455": "shortest-matching-substring",
        # "3459": "length-of-longest-v-shaped-diagonal-segment",
        # "3463": "check-if-digits-are-equal-in-string-after-operations-ii",
        # "3464": "maximize-the-distance-between-points-on-a-square",
        # "3470": "permutations-iv",
        # "3474": "lexicographically-smallest-generated-string",
        # ##################
        # "3405": "count-the-number-of-arrays-with-k-matching-adjacent-elements",
        # "3414": "maximum-score-of-non-overlapping-intervals",
        # "3420": "count-non-decreasing-subarrays-after-k-operations",
        # "3426": "manhattan-distances-of-all-arrangements-of-pieces",
        # "3441": "minimum-cost-good-caption",
    }

    # Config 1 - Baseline: Prompt is short as possible, no tests
    # Config 2 - Some unit tests provided
    # Config 3 - Some property-based tests provided
    configs = [1]

    # Get validation set
    generate_unit_tests(list_problems)

    for config in configs:
        pass
        # GET problem -> p[id]_problem.json, p[id]_config#.py
        # generate_py_problem(list_problems, config)

        # Run Pythoness -> p[id]_config#.out, p[id]_config#_#.py
        # run_pythoness(list_problems.keys(), config, 5)
        # make_solution(list_problems, config)  # -> p[id]_config#_#_pytest.py
        # Evaluate Results
        # evaluate_results(list_problems, config)


if __name__ == "__main__":
    main()
