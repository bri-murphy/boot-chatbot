import os
def get_files_info(working_directory, directory="."):
    work_abs = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(working_directory, directory))
    if not (abs_path == work_abs or abs_path.startswith(work_abs + os.sep)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_path): 
        return f'Error: "{directory}" is not a directory'
    
    directory_list =[]
    try:
        for location in sorted(os.listdir(abs_path)):
            current_path = os.path.join(abs_path, location)
            directory_list .append(f"- {location}: file_size={os.path.getsize(current_path)} bytes, is_dir={os.path.isdir(current_path)}")
        return "\n".join(directory_list)
    except Exception as e:
        return f"Error: {e}"

