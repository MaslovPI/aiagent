import os
from os import path


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = path.abspath(working_directory)
        target_dir = path.normpath(path.join(working_dir_abs, directory))
        valid_target_dir = (
            path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        if not valid_target_dir:
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
