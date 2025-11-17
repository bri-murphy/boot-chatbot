import os
from google.genai import types
def write_file(working_directory, file_path, content):
    work_abs = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not (abs_path == work_abs or abs_path.startswith(work_abs + os.sep)):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    try:
        with open(abs_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes desired string to provided file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the desired file. New file is created if that file doesn't exist in the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to file_path. If content already exists within the file, this value should overwrite it.",
            ),
        },
    ),
)