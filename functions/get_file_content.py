# functions/get_file_content.py

import os

# Define a constant for the character limit
MAX_FILE_LENGTH = 10000


def get_file_content(working_directory, file_path):
    """
    Reads the content of a file, scoped to a working directory.

    Args:
        working_directory (str): The base directory the agent is allowed to
                                 access. The "jail".
        file_path (str): The path to the file, relative to the
                         working_directory.

    Returns:
        str: The content of the file as a string, or an error message.
    """
    try:
        full_path = os.path.join(working_directory, file_path)

        # Resolve the real, absolute paths to prevent directory traversal
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        # Ensure the resolved file path is still inside the working directory
        if not abs_full_path.startswith(abs_working_dir):
            return (
                f'Error: Cannot read "{file_path}" as it is outside the '
                "permitted working directory"
            )

        if not os.path.isfile(abs_full_path):
            return (
                f'Error: File not found or is not a regular file: "{file_path}"'
            )

        with open(abs_full_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        if len(content) > MAX_FILE_LENGTH:
            truncated_content = content[:MAX_FILE_LENGTH]
            truncation_message = (
                f'\n[...File "{file_path}" truncated at {MAX_FILE_LENGTH} '
                "characters]"
            )
            return truncated_content + truncation_message

        return content

    except Exception as e:
        return f"Error: An unexpected error occurred: {e}"