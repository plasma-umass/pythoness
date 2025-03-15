import os
import re


def rename_oracle_files(directory="results"):
    pattern = re.compile(r"oracle(\d+)\.py")

    for root, _, files in os.walk(directory):
        for filename in files:
            match = pattern.fullmatch(filename)
            if match:
                number = match.group(1)
                new_filename = f"p{number}_oracle.py"
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, new_filename)

                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")


if __name__ == "__main__":
    rename_oracle_files()
