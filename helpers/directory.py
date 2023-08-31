import os


def is_directory_exist(directory_path):
    return os.path.exists(directory_path)


def create_directory(directory_path):
    try:
        # Create the directory
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
