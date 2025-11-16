import os
from config import *
def get_file_content(working_directory, file_path):
    work_abs = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not (abs_path == work_abs or abs_path.startswith(work_abs + os.sep)):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_path): 
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) == 10000:
                file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
            # print(file_content_string)
        return file_content_string
    except Exception as e:
        return f"Error: {e}"