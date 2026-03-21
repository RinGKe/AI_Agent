from functions.get_files_info import *


def test(work_dir, dir):
    if dir != ".":
        print(f"Result for '{dir}' directory:")
    else:
        print("Result for current directory:")
    print(get_files_info(work_dir, dir))
    print("\n")


test("calculator", ".")
test("calculator", "pkg")
test("calculator", "/bin")
test("calculator", "../")
