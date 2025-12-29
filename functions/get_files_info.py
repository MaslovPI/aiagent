import os
from os import path

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
