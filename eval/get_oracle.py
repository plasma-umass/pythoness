import os
import shutil
import subprocess


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


def run_coverup_in_results():
    results_dir = "results"
    specific_subdirs = [
        # "765",
        # "801",
        # "2251",
        # "2334",
        # "3312",
        # "3445",
        "3448",
        "3449",
        "3459",
    ]  # Replace with the subdirectory names you want

    if not os.path.isdir(results_dir):
        print(f"Directory '{results_dir}' does not exist.")
        return

    for subdir in specific_subdirs:

        subdir_path = os.path.join(results_dir, subdir)

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


if __name__ == "__main__":
    # Search results/i/ for "i_oracle.py" and reorganize into src/oraclei.py and empty tests/
    # organize_results()
    # RUN COVERUP ON EVERYTHING
    run_coverup_in_results()
