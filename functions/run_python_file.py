import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    work_abs = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not (abs_path == work_abs or abs_path.startswith(work_abs + os.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if file_path not in sorted(os.listdir(work_abs)):
        return f'Error: File "{file_path}" not found.'
    if file_path[-3:] != '.py':
        return f'Error: "{file_path}" is not a Python file.'
    try:
        cmd = ["python", file_path] + args
        subprocess_result = subprocess.run(cmd, timeout=30, capture_output=True, cwd=work_abs)
        return_string = f"STDOUT:{subprocess_result.stdout.decode()}\nSTDERR:{subprocess_result.stderr.decode()}"
        if subprocess_result.returncode != 0:
            return_string += f"\nProcess exited with code {subprocess_result.returncode}"
        if subprocess_result.stdout.decode() == '':
            return_string = 'No output produced.'
        return return_string
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = schema_get_file_content = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes named python file and any associated command line args passed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the desired python file. Program returns error if file can't be found in working directory, or if filename doesn't end in .py",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Optional list of command line arguments to pass to invoked file.",
            ),
        },
    ),
)