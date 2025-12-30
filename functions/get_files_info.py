import os
from os import path

from google.genai import types

from functions.normalize_path import normalize_path


def get_files_info(working_directory, directory="."):
    try:
        target_dir = normalize_path(working_directory, directory)
        if target_dir is None:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        content = os.scandir(target_dir)
        info = ""
        for file in content:
            info += f"- {file.name}: file_size={path.getsize(file)} bytes, is_dir={file.is_dir()}\n"
        return info
    except Exception as ex:
        return "Error: " + str(ex)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
