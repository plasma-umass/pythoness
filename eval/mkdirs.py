import os
import shutil


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
        new_oracle_name = os.path.join(src_path, f"oracle[{subdir}].py")

        if os.path.exists(oracle_file):
            try:
                shutil.move(oracle_file, new_oracle_name)
                print(f"Moved and renamed '{oracle_file}' to '{new_oracle_name}'")
            except Exception as e:
                print(f"Error moving '{oracle_file}' to '{src_path}': {e}")
        else:
            print(f"Warning: '{oracle_file}' not found in '{subdir}'.")


if __name__ == "__main__":
    organize_results()
