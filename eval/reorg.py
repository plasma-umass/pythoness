import os

# Define the parent directory
parent_dir = "results"

# Iterate over all subdirectories in the parent directory
for subdir in os.listdir(parent_dir):
    subdir_path = os.path.join(parent_dir, subdir)

    # Check if the subdirectory name is a number
    if os.path.isdir(subdir_path) and subdir.isdigit():
        new_name = f"p{subdir}"
        new_subdir_path = os.path.join(parent_dir, new_name)

        # Rename the subdirectory
        os.rename(subdir_path, new_subdir_path)
        print(f"Renamed {subdir} to {new_name}")
