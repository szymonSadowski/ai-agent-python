import os
import subprocess
def run_python_file(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)

        # Resolve the real, absolute paths to prevent directory traversal
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        # Ensure the resolved file path is still inside the working directory
        if not abs_full_path.startswith(abs_working_dir):
            return (
                f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            )
        if not os.path.isfile(abs_full_path):
            return f'Error: File "{file_path}" not found.'
        if not full_path.endswith('.py'):
            return  f'Error: "{file_path}" is not a Python file.'

        # --- Execute the File ---
        result = subprocess.run(
            ["python3", file_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_directory,  # Execute from within the jail
        )

                
        output_parts = []
        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout.strip()}")
        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr.strip()}")
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not output_parts:
            return "No output produced."

        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds."
    except Exception as e:
        return f"Error: executing Python file: {e}"