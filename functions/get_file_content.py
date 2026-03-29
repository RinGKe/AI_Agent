import os

from config import *


def get_file_content(working_directory, file_path, size=MAX_CHARS):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, file_path))
        if os.path.commonpath([abs_path, target_dir]) != abs_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_dir) as file:
            content = file.read(size)
            if file.read(1):
                content += f' [...File "{file_path}" truncated at {size} characters]'
            return content

    except Exception as e:
        return f"Error listing files: {e}"
