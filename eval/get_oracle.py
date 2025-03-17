import os
import shutil
import subprocess
import re
import glob


def organize_results(subdirs=None):
    base_dir = "results"

    all_subdirs = [
        d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))
    ]

    # If no specific subdirectories are provided, loop over all
    subdirs = specific_subdirs if specific_subdirs is not None else all_subdirs

    for subdir in subdirs:
        subdir_path = os.path.join(base_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue  # Skip non-directory entries

        src_path = os.path.join(subdir_path, "src")
        tests_path = os.path.join(subdir_path, "tests")

        # Make dirs src and tests if not already existing
        try:
            os.makedirs(src_path, exist_ok=True)
            os.makedirs(tests_path, exist_ok=True)
        except Exception as e:
            print(f"Error creating directories in '{subdir}': {e}")
            continue

        # Get the oracle file
        base_dir = "../../LeetCode/solutions/"
        list = os.listdir(base_dir)
        filtered = [s for s in list if s.startswith(f"{subdir}.")]

        if filtered:
            target_dir = os.path.join(base_dir, filtered[0])
            python_files = [
                file for file in os.listdir(target_dir) if file.endswith(".py")
            ]
            if python_files:

                oracle_file = os.path.join(target_dir, python_files[0])
                new_oracle_name = os.path.join(src_path, f"p{subdir}oracle.py")

                try:
                    shutil.move(oracle_file, new_oracle_name)
                    print(f"Copied '{oracle_file}' to '{new_oracle_name}'")
                except Exception as e:
                    print(f"Error moving '{oracle_file}' to '{src_path}': {e}")
            else:
                print("No Python files found in", target_dir)
        else:
            print(f"No directory starting with '{subdir}.' found in {base_dir}")


def run_coverup(specific_subdirs):

    for subdir in specific_subdirs:

        subdir_path = os.path.join("results", subdir)

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


if __name__ == "__main__":
    # specific_subdirs = [  # No coverage dirs
    #     # "765",
    #     # "801",
    #     # "2251",
    #     # "2334",
    #     # "3312",
    #     # "3445",
    #     # "3448",
    #     # "3449",
    #     # "3459",
    #     "3197",
    # ]
    specific_subdirs = [  # Coverage dirs
        # "4",
        # "10",
        # "30",
        # "32",
        # "37",
        # "41",
        # "42",
        # "44",
        # "51",
        # "466"
        # "493",
        # "552",
        # "600",
        # "668",
        # "699",
        # "850",
        # "871",
        # "902",
        # "1416",
        # "1923",
        # "2872",
        # "3455",
        # "3463",
        # "3470",
    ]

    config = 1
    # Search results/i/ for "i_oracle.py" and reorganize into src/oraclei.py and empty tests/
    # organize_results(specific_subdirs)
    # Run coverup
    run_coverup(specific_subdirs)
    # Copies pytest files, and modifies and evals each run
    # setup_pytest_and_evaluate(config, specific_subdirs)
