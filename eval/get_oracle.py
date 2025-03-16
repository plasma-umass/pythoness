import os
import shutil
import subprocess
import re
import glob


def organize_results(base_dir="results"):
    if not os.path.exists(base_dir):
        print(f"Error: Directory '{base_dir}' does not exist.")
        return

    for subdir in os.listdir(base_dir):
        subdir_path = os.path.join(base_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue  # Skip non-directory entries

        src_path = os.path.join(subdir_path, "src")
        tests_path = os.path.join(subdir_path, "tests")

        try:
            os.makedirs(src_path, exist_ok=True)
            os.makedirs(tests_path, exist_ok=True)
            print(f"Created directories: {src_path}, {tests_path}")
        except Exception as e:
            print(f"Error creating directories in '{subdir}': {e}")
            continue

        oracle_file = os.path.join(subdir_path, f"{subdir}_oracle.py")
        new_oracle_name = os.path.join(src_path, f"oracle{subdir}.py")

        if os.path.exists(oracle_file):
            try:
                shutil.move(oracle_file, new_oracle_name)
                print(f"Moved and renamed '{oracle_file}' to '{new_oracle_name}'")
            except Exception as e:
                print(f"Error moving '{oracle_file}' to '{src_path}': {e}")
        else:
            print(f"Warning: '{oracle_file}' not found in '{subdir}'.")


def run_coverup_in_results(specific_subdirs):

    for subdir in specific_subdirs:

        subdir_path = os.path.join("results", subdir)

        # if os.path.exists(os.path.join(subdir_path, "coverup-log")):
        #     print("Coverup already run here. Skip.")
        #     continue

        if os.path.isdir(subdir_path):
            print(f"Entering {subdir_path} and running coverup...")

            process = subprocess.Popen(
                ["coverup", "--package", "src", "--tests-dir", "tests"],
                cwd=subdir_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            for line in process.stdout:
                print(line, end="")  # Print output as it arrives

            process.wait()
            print(f"Finished running coverup in {subdir_path}\n")
            # Define source and destination directories

            source_pattern = f"{subdir_path}/tests/test_coverup_*.py"

            # Ensure destination directory exists
            os.makedirs(subdir_path, exist_ok=True)

            # Make a copy of all coverup files
            for file_path in glob.glob(source_pattern):
                file_name = os.path.basename(file_path)
                destination_path = os.path.join(subdir_path, file_name)
                shutil.copy(file_path, destination_path)
                print(f"Copied {file_path} to {destination_path}")


def modify_test_file(test_file, new_solution_import):
    with open(test_file, "r") as f:
        content = f.read()

    # Step 1: Find the existing import statement and extract the original solution import
    solution_import_pattern = r"from\s+([\w\.]+)\s+import\s+Solution"
    match = re.search(solution_import_pattern, content)

    if not match:
        print("Error: Could not find the original Solution import statement.")
        return

    original_module = match.group(1)  # e.g., "src.oracle4"

    # Step 2: Modify imports to include the second implementation
    modified_imports = (
        f"from {original_module} import Solution as Solution1\n"
        f"from {new_solution_import} import Solution as Solution2\n"
    )

    content = re.sub(solution_import_pattern, modified_imports, content, count=1)

    # Step 3: Modify the pytest fixture to test both implementations
    fixture_pattern = r"@pytest\.fixture\ndef solution\(\):\n\s+return Solution\(\)"

    modified_fixture = (
        "@pytest.fixture(params=[Solution1, Solution2])\n"
        "def solution(request):\n"
        "    return request.param()\n"
    )

    content = re.sub(fixture_pattern, modified_fixture, content)

    # Step 4: Save the modified test file
    with open(test_file, "w") as f:
        f.write(content)

    print(f"Successfully modified {test_file} to compare both implementations.")


def evaluate(config: int, specific_subdirs=None):
    parent_dir = "results"
    # Get full paths of all subdirectories
    all_subdirs = [
        d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))
    ]

    # If no specific subdirectories are provided, loop over all
    subdirs = specific_subdirs if specific_subdirs is not None else all_subdirs

    for subdir in subdirs:

        subdir_path = os.path.join("results", subdir)

        if os.path.isdir(subdir_path):
            print(f"Entering {subdir_path} and evaluating config {config}...")

            # Define the file pattern
            file_pattern = f"p{id}_config{config}_*_pytest.py"
            file_path_pattern = os.path.join(subdir_path, file_pattern)

            # Loop over matching files
            for file in glob.glob(file_path_pattern):
                print(f"  Found file: {file}")
                # Add your file processing logic here


if __name__ == "__main__":
    # Search results/i/ for "i_oracle.py" and reorganize into src/oraclei.py and empty tests/
    # organize_results()
    specific_subdirs = [  # No coverage dirs
        # "765",
        # "801",
        # "2251",
        # "2334",
        # "3312",
        # "3445",
        # "3448",
        # "3449",
        # "3459",
    ]
    specific_subdirs = [  # Coverage dirs
        "4",
        # "10",
        # "30",
        # "32",
        # "37",
        # "41",
        # "42",
        # "44",
        # "51",
    ]

    config = 1
    # Run coverup (run from eval folder)
    # run_coverup_in_results(specific_subdirs)
    # Example usage
    evaluate(config, specific_subdirs)
    # modify_test_file(
    #     "results/p4/test_coverup_1.py", "results/p4/4_config1_1.py"
    # )  # Replace with actual test filename and new implementation module
