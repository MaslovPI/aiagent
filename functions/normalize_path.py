from os import path


def normalize_path(working_directory, path_to_normalize):
    working_dir_abs = path.abspath(working_directory)
    target_path = path.normpath(path.join(working_dir_abs, path_to_normalize))
    valid_target = path.commonpath([working_dir_abs, target_path]) == working_dir_abs

    if valid_target:
        return target_path
    return None
