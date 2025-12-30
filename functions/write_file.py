import os

from google.genai import types
from functions.normalize_path import normalize_path


def write_file(working_directory, file_path, content):
    try:
        target_path = normalize_path(working_directory, file_path)
        if target_path is None:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = os.path.dirname(target_path)
        os.makedirs(parent_dir, exist_ok=True)
        file_stream = open(target_path, mode="w+")
        file_stream.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as ex:
        return f"Error: {str(ex)}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text content to a specified file within the working directory (overwriting if the file exists)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
