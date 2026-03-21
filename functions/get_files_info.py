import os


def get_files_info(work_directory, directory="."):
    try:
        abs_path = os.path.abspath(work_directory)
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
