import os
from config import MAX_CHARS
from functions.normalize_path import normalize_path


def get_file_content(working_directory, file_path):
    try:
        target_path = normalize_path(working_directory, file_path)
        if target_path is None:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        file_stream = open(target_path)
        file_content = file_stream.read(MAX_CHARS)

        if file_stream.read(1):
            file_content += (
                f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            )
        return file_content
    except Exception as ex:
        return f"Error: {str(ex)}"
