from __future__ import annotations

import util.setup as setup
import util.query as query

import glob
import os
import re
import shutil
import subprocess
import json


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


def evaluate_results(specific_subdirs, config):

    for subdir in specific_subdirs:

        subdir_path = os.path.join("results", subdir)

        # Load the tests file data
        test_file = os.path.join(subdir_path, f"p{subdir}_tests.json")
        with open(test_file, "r") as f:
            test_data = json.load(f)

        validation_indices = test_data["validation"]
        test_inputs = test_data["inputs"]
        test_outputs = test_data["outputs"]
        inputs = [test_inputs[i] for i in validation_indices]
        expected_outputs = [test_outputs[i] for i in validation_indices]

        # Modify list of tests run by runner
        print("Modifying runner...")
        runner_file = f"p{subdir}_test_runner.py"
        runner_file_path = os.path.join(subdir_path, runner_file)
        with open(runner_file_path, "r") as f:
            lines = f.readlines()

        # Replace inputs list
        for i, line in enumerate(lines):
            if line.startswith("inputs"):
                lines[i] = f"inputs_list = {inputs}\n"
                break

        # Write the modified content back to the file
        with open(runner_file_path, "w") as f:
            f.writelines(lines)

        # Iterate over all runs of this config
        file_pattern = f"p{subdir}_config{config}_*.py"
        pytests_pattern = os.path.join(subdir_path, file_pattern)
        pytests = glob.glob(pytests_pattern)

        # pytests = [
        #     "./results/3449/p3449_config1_2.py",
        #     "./results/3449/p3449_config1_4.py",
        # ]

        for py in pytests:

            with open(py, "r") as f:
                code = f.read()
            if code.find('""""""') != -1:
                print(f"Pythoness failed for {py}! Skipping.")
                test_data[os.path.basename(py)] = []
                test_data[f"{os.path.basename(py)}_results"] = (
                    f"Pythoness failed, no results available"
                )
                continue

            with open(runner_file_path, "r") as f:
                lines = f.readlines()

            # Loop through lines to find the first one starting with "import src"
            for i, line in enumerate(lines):
                if line.startswith(f"from p{subdir}oracle") or line.startswith(
                    f"from p"
                ):
                    lines[i] = f"from {os.path.basename(py)[:-3]} import Solution\n"
                if line.startswith("inputs"):
                    lines[i] = f"inputs_list = {inputs}\n"
                    break

            # Write the modified content back to the file
            with open(runner_file_path, "w") as f:
                f.writelines(lines)

            print(f"Evaluating {py}...")

            result = subprocess.run(
                ["python3", runner_file_path],
                capture_output=True,
                text=True,
            )
            results = result.stdout.splitlines()
            test_data[os.path.basename(py)] = results

            # print(results)
            # print(expected_outputs)

            passed = 0
            error = 0
            for t in list(range(10)):
                if expected_outputs[t] == results[t]:
                    passed += 1
                elif (
                    subdir == "3454"
                    and abs(float(expected_outputs[t]) - float(results[t])) < 1e-5
                ):
                    passed += 1
                elif results[t].startswith("Input failed: "):
                    error += 1

            test_data[f"{os.path.basename(py)}_results"] = (
                f"{passed} PASSED, {10 - passed} FAILED, {error} ERRORS"
            )

        # Write the result to the test file
        with open(test_file, "w") as f:
            json.dump(test_data, f, indent=4)


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

    # Config 1 - Baseline: Prompt is short as possible, no tests
    # Config 2 - Half unit tests provided
    # Config 3 - Pythoness allowed to LLM-generate property-based tests
    configs = [1]

    # GET problem -> p[id]_problem.json, p[id]oracle.py
    # setup.get_problem(list_problems)
    # # Generate GPT input/s, run oracle -> p[id]_tests.json, p[id]_test_runner.py
    # setup.generate_unit_tests(list_problems)
    # # Once all validated, split tests
    # setup.separate_gen_and_valid_tests(list_problems)

    for config in configs:
        pass
        # Generate config files -> p[id]_config#.py
        # setup.generate_py_problems(list_problems, config)
        # # Run Pythoness -> p[id]_config#.out, p[id]_config#_#.py
        run_pythoness(list_problems, config, 1)
        # Evaluate Results
        # evaluate_results(list_problems, config)


if __name__ == "__main__":
    main()
