import os

from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, directory))
        if os.path.commonpath([abs_path, target_dir]) != abs_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            if not os.path.isdir(target_dir):
                return f'Error: "{directory}" is not a directory'

        file_list = []
        for file in os.listdir(target_dir):
            path = os.path.join(target_dir, file)
            file_size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            file_list.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(file_list)
    except Exception as e:
        return f"Error listing files: {e}"


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
        required=["directory"],
    ),
)
