from functions.get_file_content import get_file_content
print('Test Case 1:')
print(get_file_content("calculator", "main.py"))
print('Test Case 2:')
print(get_file_content("calculator", "pkg/calculator.py"))
print('Test Case 3:')
print(get_file_content("calculator", "/bin/cat")) #(this should return an error string)
print('Test Case 4:')
print(get_file_content("calculator", "pkg/does_not_exist.py")) #(this should return an error string)