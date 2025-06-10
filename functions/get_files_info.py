# functions/get_files_info.py

import os


def get_files_info(working_directory, directory=None):
    """
    Lists the contents of a directory and its metadata as a formatted string.

    Args:
        working_directory (str): The base directory the agent is allowed to
                                 access. The "jail".
        directory (str, optional): The specific directory to list, relative
                                   to the working_directory. Defaults to the
                                   working_directory itself.

    Returns:
        str: A formatted string of the directory contents or an error message.
    """
    try:
        # Determine the target path to list
        if directory is None:
            # If no specific directory is given, use the root of the jail
            target_path = working_directory
        else:
            # If a directory is given, join it with the jail's path
            target_path = os.path.join(working_directory, directory)

        # --- Security Check ---
        # Resolve the real, absolute paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(target_path)

        # Ensure the resolved target path is still inside the working directory
        if not abs_target_path.startswith(abs_working_dir):
            return (
                f'Error: Cannot list "{directory}" as it is outside the '
                "permitted working directory"
            )

        # --- Path Validation ---
        if not os.path.isdir(abs_target_path):
            return f'Error: "{directory or "."}" is not a directory'

        # --- Build the Output String ---
        output_lines = []
        for item_name in sorted(os.listdir(abs_target_path)):
            item_path = os.path.join(abs_target_path, item_name)
            stats = os.stat(item_path)
            is_dir = os.path.isdir(item_path)
            file_size = stats.st_size

            output_lines.append(
                f"- {item_name}: file_size={file_size} bytes, is_dir={is_dir}"
            )

        if not output_lines:
            return "Directory is empty."

        return "\n".join(output_lines)

    except Exception as e:
        # Catch any other potential OS errors (e.g., permission denied)
        return f"Error: {e}"