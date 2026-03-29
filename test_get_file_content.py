from functions.get_file_content import *

print(get_file_content("calculator", "main.py", 15))
print(get_file_content("calculator", "pkg/calculator.py", 1250))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))
