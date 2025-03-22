import os
import re
import json
from time import sleep

from query import get_problem_details


def get_function_name(code):
    matches = re.findall(r"\bdef\s+(\w+)", code)  # Finds all function names
    if matches:
        return matches[-1]  # Returns the last function name
    else:
        return None  # Returns None if no match is found


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


def generate_json_problem(list_problems: dict, id) -> dict:
    if isinstance(list_problems[id], tuple):
        name = list_problems[id][0]
    else:
        name = list_problems[id]

    # Get problem details, write to json
    details = get_problem_details(name)

    if not os.path.exists(f"./results/{id}"):
        os.makedirs(f"./results/{id}")

    with open(f"./results/{id}/p{id}_problem.json", "w") as json_file:
        json.dump(details, json_file, indent=4)

    # Take a break between GET requests
    sleep(5)

    return details


def generate_py_problem(list_problems: dict, config: int) -> str:
    i = 0
    tot = len(list_problems)
    for id, name in list_problems.items():
        i += 1

        print(f"Creating p{id}_config{config}.py... {i}/{tot}")

        if not os.path.exists(f"./results/{id}"):
            os.makedirs(f"./results/{id}")

        # Retrieve prompt and template code
        if os.path.exists(f"./results/{id}/p{id}_problem.json"):
            with open(f"./results/{id}/p{id}_problem.json", "r") as file:
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
        if config > 4:
            all_unittests = ""
        else:
            all_unittests = ", ".join([f"'{i}'" for i in unittests])

        # Remove examples
        prompt = re.sub(r"\nExample 1.*?(?=\nConstraints)", "", prompt, flags=re.DOTALL)
        # Remove Constraints
        # if config > 5:
        #     prompt = prompt[: prompt.find("\nConstraints:")].strip()
        # Insert tests
        # content = re.sub(r"tests=\[\]", f"tests=[{all_unittests}]", content)

        # Save original prompt
        with open(f"./results/{id}/p{id}_prompt_full.txt", "w") as prompt_file:
            prompt_file.write(prompt)

        # Remove any Follow-up section
        index = prompt.find("\nFollow-up:")
        prompt = prompt[:index].strip() if index != -1 else prompt

        # Forget above - get prompt from prompt file
        with open(f"./results/{id}/p{id}_prompt.txt", "r") as prompt_file:
            prompt = prompt_file.read()

        # Insert prompt as func docstring
        # if config != 7:
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
                # content = content.replace(
                #     "time_bound=None,",
                #     f'time_bound="{matches[0]}",\n    range=(),',
                # )
            else:
                print("Multiple runtime bound match")

        # Write full program to id_config#.py
        with open(f"./results/{id}/p{id}_config{config}.py", "w") as target_file:
            target_file.write(content)
