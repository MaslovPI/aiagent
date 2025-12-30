import subprocess
from os import path

from google.genai import types
from functions.normalize_path import normalize_path


def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = path.abspath(working_directory)
        target_path = normalize_path(working_directory, file_path)
        if target_path is None:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        (_, ext) = path.splitext(target_path)
        if not (ext == ".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]
        if args is not None:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output)
    except Exception as ex:
        return f"Error: executing Python file: {ex}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file within the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of arguments to pass to the Python script",
            ),
        },
        required=["file_path"],
    ),
)
