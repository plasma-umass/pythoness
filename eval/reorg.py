import os


def rename_subdirs(parent_dir="results"):
    # Ensure the parent directory exists
    if not os.path.exists(parent_dir):
        print(f"Parent directory '{parent_dir}' does not exist.")
        return

    # Loop over all subdirectories
    for subdir in os.listdir(parent_dir):
        subdir_path = os.path.join(parent_dir, subdir)

        # Check if it's a directory and starts with "p"
        if os.path.isdir(subdir_path) and subdir.startswith("p"):
            new_name = subdir[1:]  # Remove the leading "p"
            new_path = os.path.join(parent_dir, new_name)

            # Ensure the new name does not already exist
            if os.path.exists(new_path):
                print(
                    f"Cannot rename '{subdir}' to '{new_name}' because '{new_name}' already exists."
                )
            else:
                os.rename(subdir_path, new_path)
                print(f"Renamed '{subdir}' to '{new_name}'")


# Run the function
rename_subdirs()
