import os
import re
import json
import shutil
from time import sleep
import subprocess
import random

from . import query
from . import assistant


# def _query_inputs(prompt, subdir, test_file_path):
#     print(f"Prompting GPT for unit tests for {subdir}...")
#     client = assistant.Assistant()

#     result = client.query(prompt)

#     # Get inputs list and write to tests.json file
#     try:
#         inputs_list = json.loads(result)["inputs"]

#         with open(test_file_path, "r") as json_file:
#             data = json.loads(json_file.read())
#         existing_inputs = data["inputs"]
#         if len(existing_inputs) >= 20:
#             data["inputs"] = inputs_list
#         else:
#             data["inputs"] = existing_inputs + inputs_list
#         with open(test_file_path, "w") as json_file:
#             json.dump(data, json_file, indent=4)
#     except (json.JSONDecodeError, KeyError, TypeError) as e:
#         print("Error parsing JSON:", e)


def get_problem_details(list_problems: dict, id: str) -> dict:
    if os.path.exists(f"./results/{id}/p{id}_problem.json"):
        with open(f"./results/{id}/p{id}_problem.json", "r") as file:
            details = json.load(file)
    else:
        details = query.get_problem_details(list_problems[id])
        with open(f"./results/{id}/p{id}_problem.json", "w") as json_file:
            json.dump(details, json_file, indent=4)
        # Take a break between GET requests
        sleep(5)
    return details


def get_function_name(list_problems, id):
    details = get_problem_details(list_problems, id)
    matches = re.findall(
        r"\bdef\s+(\w+)", details["template_code_definition"]
    )  # Finds all function names
    if matches:
        return matches[-1]  # Returns the last function name
    else:
        return None  # Returns None if no match is found


def get_id(list_problems, id):
    details = get_problem_details(list_problems, id)

    return details["id"]


def get_problem(list_problems: dict) -> None:
    for id, name in list_problems.items():
        print(f"Creating p{id}_problem.json...")

        os.makedirs(f"./results/{id}", exist_ok=True)

        # Retrieve prompt and template code
        details = get_problem_details(list_problems, id)

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

        # Remove examples
        prompt = re.sub(r"\nExample 1.*?(?=\nConstraints)", "", prompt, flags=re.DOTALL)
        # Remove Constraints
        # prompt = prompt[: prompt.find("\nConstraints:")].strip()
        # Insert tests
        # content = re.sub(r"tests=\[\]", f"tests=[{all_unittests}]", content)

        # # Remove any Follow-up section
        index = prompt.find("\nFollow-up:")
        prompt = prompt[:index].strip() if index != -1 else prompt

        # Save original prompt
        with open(f"./results/{id}/p{id}_prompt_full.txt", "w") as prompt_file:
            prompt_file.write(prompt)

        # # Searching for oracle file
        # solutions_dir = os.path.abspath("../../LeetCode/solutions")

        # # Find a directory starting with "id."
        # matching_dirs = [
        #     d
        #     for d in os.listdir(solutions_dir)
        #     if os.path.isdir(os.path.join(solutions_dir, d)) and d.startswith(f"{id}.")
        # ]

        # if not matching_dirs:
        #     print("No directory starting with 'id.' found.")
        # else:
        #     # Use the first matching directory found
        #     target_dir = os.path.join(solutions_dir, matching_dirs[0])

        #     # Find the first .py file in the directory
        #     py_files = [f for f in os.listdir(target_dir) if f.endswith(".py")]

        #     if not py_files:
        #         print("No .py file found in the target directory.")
        #     else:
        #         # Copy the first .py file to ./results
        #         results_dir = f"./results/{id}/"
        #         shutil.copy(
        #             os.path.join(target_dir, py_files[0]),
        #             os.path.join(results_dir, f"p{id}oracle.py"),
        #         )

        #         print(f"Copied p{id}oracle.py")


def generate_py_problems(list_problems: dict, config: int) -> str:
    i = 0
    tot = len(list_problems)
    for id, name in list_problems.items():
        i += 1

        print(f"Creating p{id}_config{config}.py... {i}/{tot}")

        details = get_problem_details(list_problems, id)

        prompt = details["problem_statement"].replace("\xa0", "")
        template = details["template_code_snippet"]

        if config == 1 or config == 2:
            template_insert = "\n    llm_unit=False,\n    llm_prop=False,"
        elif config == 3:
            template_insert = "\n    llm_prop=False,"
        # elif config == 4:
        # template_insert = "\n    runtime=True,"
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

        # # Extract examples as unit tests
        func_name = get_function_name(list_problems, id)

        with open(f"./results/{id}/p{id}_tests.json", "r") as json_file:
            data = json.load(json_file)

        inputs = data["inputs"]
        outputs = data["outputs"]
        indices = data["generation"]

        inputs = [inputs[i] for i in indices]
        outputs = [outputs[i] for i in indices]

        unittests = []
        for i in range(len(inputs)):
            string = f"{func_name}(**{inputs[i]}) == "
            if isinstance(outputs[i], str):
                string += f"'{outputs[i]}'"
            else:
                string += str(outputs[i])
            unittests.append(string)

        if config > 4:
            all_unittests = ""
        else:
            all_unittests = ", ".join([f'"""{i}"""' for i in unittests])

        # Insert tests
        if config > 1:
            content = re.sub(r"tests=\[\]", f"tests=[{all_unittests}]", content)

        # Get prompt from prompt file
        with open(f"./results/{id}/p{id}_prompt.txt", "r") as prompt_file:
            prompt = prompt_file.read()

        # Insert prompt as func docstring
        index = content.find('"""')
        content = content[: index + 3] + prompt.strip() + content[index + 3 :]
        # Replace call to foo

        content = content.replace(
            "dummy_func()",
            unittests[0][: unittests[0].find("==")].replace("({", "(**{", 1),
        )

        # Find all O() mentions
        pattern = r"O\((?:[^()]*|(?:[^()]*\([^()]*\)))*\)"
        matches = re.findall(pattern, prompt)
        if len(matches) > 0:
            if len(matches) == 1:
                print("One runtime bound match")
            else:
                print("Multiple runtime bound match")

        # Write full program to id_config#.py
        with open(f"./results/{id}/p{id}_config{config}.py", "w") as target_file:
            target_file.write(content)


def generate_unit_tests(list_problems):
    specific_subdirs = list_problems.keys()
    for subdir in specific_subdirs:
        subdir_path = os.path.join("results", subdir)
        test_file = f"p{subdir}_tests.json"
        test_file_path = os.path.join(subdir_path, test_file)

        # Get func_name
        func_name = get_function_name(list_problems, subdir)

        with open(os.path.join(subdir_path, f"p{subdir}_prompt_full.txt"), "r") as f:
            docstring = f.read().strip()

        with open(os.path.join(subdir_path, f"p{subdir}oracle.py"), "r") as f:
            func = f.read()

        for line in func.splitlines():
            if line.lstrip().startswith(f"def {func_name}"):
                func = line.strip() + f'\n    """{docstring}"""'
                break

        # Ask GPT for validation set
        prompt = (
            f"""Generate 5 diverse inputs to test the following function signature and description:\n\n```\n"""
            + func
            + "\n```\n"
            + """Return the result as a JSON object with the following structure:
```
{  
  "inputs": [  
    {"arg_name": value1, "arg_name": value2, ...},  
    {"arg_name": value3, "arg_name": value4, ...},  
    ... (5 entries)  
  ]  
}
```"""
        )

        # print(prompt)

        # _query_inputs(prompt, subdir, test_file_path)

        with open(test_file_path, "r") as file:
            data = json.load(file)
        inputs_list = data["inputs"]

        print("Running oracle and collecting unit tests...")
        # Run ground truth and collect results
        runner = os.path.join(subdir_path, f"p{subdir}_test_runner.py")
        with open(runner, "w") as f:
            f.write(
                f"""
from p{subdir}oracle import Solution

inputs_list = {inputs_list}

for i in range(len(inputs_list)):
    try:
        print(Solution().{func_name}(**inputs_list[i]))
    except Exception as e:
        print("Input failed: ", inputs_list[i], "    Error: ", e)
"""
            )

        result = subprocess.run(
            ["python3", runner],
            capture_output=True,
            text=True,
        )

        data["outputs"] = result.stdout.splitlines()

        # Write the result to the test file
        print("Writing to", test_file)
        try:
            with open(test_file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)
        except Exception as e:
            print("Error writing to file:", e)


def separate_gen_and_valid_tests(list_problems):
    specific_subdirs = list_problems.keys()
    for subdir in specific_subdirs:
        subdir_path = os.path.join("results", subdir)
        test_file = f"p{subdir}_tests.json"
        test_file_path = os.path.join(subdir_path, test_file)

        print(f"Separating {subdir} tests into generation and validation sets...")

        with open(test_file_path, "r") as file:
            data = json.load(file)

        numbers = list(range(20))

        # Shuffle the list to randomize the order
        random.shuffle(numbers)

        # Split the list into two lists of size 10 each
        list1 = numbers[:10]
        list2 = numbers[10:]

        # Create a dictionary with the two lists as values
        data["generation"] = sorted(list1)
        data["validation"] = sorted(list2)

        with open(test_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
