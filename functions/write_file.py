# functions/write_file.py

import os


def write_file(working_directory, file_path, content):
    """
    Writes or overwrites a file with the given content, scoped to a
    working directory.

    Args:
        working_directory (str): The base directory the agent is allowed to
                                 access. The "jail".
        file_path (str): The path to the file, relative to the
                         working_directory.
        content (str): The content to write to the file.

    Returns:
        str: A success or error message.
    """
    try:
        # --- Security Check ---
        # Join the working directory and file path to get the full target path
        full_path = os.path.join(working_directory, file_path)

        # Resolve the real, absolute paths to prevent directory traversal
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        # Ensure the resolved file path is still inside the working directory
        if not abs_full_path.startswith(abs_working_dir):
            return (
                f'Error: Cannot write to "{file_path}" as it is outside the '
                "permitted working directory"
            )

        # --- Write File ---
        # Create parent directories if they don't exist.
        # For example, if writing to 'pkg/morelorem.txt', this creates 'pkg'.
        parent_dir = os.path.dirname(abs_full_path)
        os.makedirs(parent_dir, exist_ok=True)

        # Write the content to the file, overwriting it if it exists.
        with open(abs_full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" '
            f"({len(content)} characters written)"
        )

    except IsADirectoryError:
        return f'Error: Cannot write to "{file_path}" because it is a directory.'
    except Exception as e:
        return f"Error: An unexpected error occurred: {e}"