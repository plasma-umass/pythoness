from __future__ import annotations

from time import sleep
from query import get_problem_details, submit_solution

import json
import os
import re
import shutil
import subprocess

# Get from browser cookies
# SESSION = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTU2MjIxMDEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0YzU1ODI3MmI4MWYyMGI2MTI5MGRjM2M1ODdmNzllYzkxZWYyMWM2N2YzZDI4ODQzNDY1OWRiMDUwNDhmYjJjIiwic2Vzc2lvbl91dWlkIjoiMjEwZjA1NDMiLCJpZCI6MTU2MjIxMDEsImVtYWlsIjoia3lsYS5sZXZpbkBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImtobGV2aW4iLCJ1c2VyX3NsdWciOiJraGxldmluIiwiYXZhdGFyIjoiaHR0cHM6Ly9hc3NldHMubGVldGNvZGUuY29tL3VzZXJzL2tobGV2aW4vYXZhdGFyXzE3MzE3MjQzMjgucG5nIiwicmVmcmVzaGVkX2F0IjoxNzQxMzY0MTA4LCJpcCI6IjEyOC4xMTkuNDAuMTk2IiwiaWRlbnRpdHkiOiI2ZGJiMTA5NTJhMzhjMTFkMTllMjY0ODAyM2Q1MDU1YiIsImRldmljZV93aXRoX2lwIjpbImFiNGM0Mjg3NGYzMDQzNGEwYmNhM2MxY2UxNTNkNmMyIiwiMTI4LjExOS40MC4xOTYiXX0.tNOvbMpoyc525wO3U9b7PA4d3xcWoaBzC1ZdKrOOqY4"
# CSRF = "AgRlMyz6zKAphcqcgSNwf9JDtncqsAoLnCeYFYOYTfbh7WtQueK6lojOkjOaxIQU"


def extract_examples(text, func_name):
    pattern = r"Input: (.*?)\n.*?Output: (.*?)\n"
    matches = re.findall(pattern, text, re.DOTALL)
    # Find all matches in the input string
    # print(matches)
    results = []
    for inputs, output in matches:
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


def generate_json_problem(list_problems: dict, id) -> dict:
    name = list_problems[id]

    # Get problem details, write to json
    details = get_problem_details(name)

    if not os.path.exists(f"./results/{id}"):
        os.makedirs(f"./results/{id}")

    with open(f"./results/{id}/{id}_problem.json", "w") as json_file:
        json.dump(details, json_file, indent=4)

    # Take a break between GET requests
    sleep(3)

    return details


def generate_py_problem(list_problems: dict, config: str) -> None:
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
        prompt = details["problem_statement"]
        # print(prompt)
        template = details["template_code_definition"]

        # Overwrite test.py with template code and insert chosen config
        with open("pythoness_template.txt", "r") as template_file:
            content = template_file.read()
        content = content.replace("tests=[],", "tests=[]," + config)
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

        # Write full program to test.py
        with open(f"./results/{id}/{id}.py", "w") as target_file:
            target_file.write(content)


def run_pythoness(ids: list) -> None:
    for id in ids:
        i = 0
        while i < 5:
            i += 1
            print(f"Running iteration {i} of Pythoness on {id}.py...")

            # Create file for output Python code, replacing it if necessary
            out_file = f"./results/{id}/{id}_{i}.py"
            if os.path.exists(out_file):
                os.remove(out_file)
            shutil.copy(f"./results/{id}/{id}.py", out_file)

            # Open the file for writing the output
            with open(f"./results/{id}/{id}.out", "w") as file:
                # Run the process and capture stdout
                process = subprocess.Popen(
                    [
                        "python3",
                        f"./results/{id}/{id}_{i}.py",
                    ],  # Replace with your command
                    stdout=subprocess.PIPE,  # Capture stdout
                    stderr=subprocess.PIPE,  # Capture stderr if needed
                    text=True,  # Ensure output is in text format (not bytes)
                )

                # Read and print the output line by line
                for line in process.stdout:
                    print(line, end="")  # Print to terminal
                    file.write(line)  # Write to the file

                # Wait for the process to finish
                process.stdout.close()
                process.wait()


def check_solution(list_problems: dict) -> dict:
    pass
    # for id, name in list_problems.items():
    #     i += 1
    #     print(f"Getting {id} {name}.json... {i}/{tot}")

    #     # Get problem details, write to json
    #     s_details = submit_solution(name, id)
    #     s_details[id] = s_details

    #     with open(f"./results/{id}/{id}_solution.json", "w") as json_file:
    #         json.dump(s_details, json_file, indent=4)

    #     # Take a break between GET requests
    #     sleep(3)

    # return s_details


def main():
    list_problems = {
        # "4": "median-of-two-sorted-arrays",
        # "10": "regular-expression-matching",
        # "23": "merge-k-sorted-lists",
        # "25": "reverse-nodes-in-k-group",
        # "30": "substring-with-concatenation-of-all-words",
        # "32": "longest-valid-parentheses",
        # "37": "sudoku-solver",
        # "41": "first-missing-positive",
        # "42": "trapping-rain-water",
        # "44": "wildcard-matching",
        "51": "n-queens",
    }
    # with open("short_questions_list.json", "r") as file:
    #     list_problems = json.load(file)  # Load the JSON data into a dictionary

    # Now, `data` is a Python dictionary
    # print(list_problems)

    template_1 = "\n    llm_unit=False,\n    llm_prop=False,"
    template_2 = "\n    llm_prop=False,"
    template_3 = ""
    template_4 = "\n    runtime=True,"
    generate_py_problem(list_problems, template_1)
    # run_pythoness(list_problems.keys())
    # check_solution()


if __name__ == "__main__":
    main()
