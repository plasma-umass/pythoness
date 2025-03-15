import os
import re


def rename_files(directory):
    pattern = re.compile(
        r"^(\d+_.*)"
    )  # Matches files starting with a number followed by _

    for root, _, files in os.walk(directory):
        for filename in files:
            if pattern.match(filename):
                old_path = os.path.join(root, filename)
                new_filename = "p" + filename
                new_path = os.path.join(root, new_filename)
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")


if __name__ == "__main__":
    rename_files("results")
