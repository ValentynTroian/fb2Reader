import glob, os


def change_dir():
    os.chdir('./res')


def fb2_file_search():
    fb2_file_list = {file for file in glob.glob("*.fb2")}
    return fb2_file_list


def incorrect_file_search():
    file_list = {file for file in glob.glob("*.*") if file not in glob.glob("*.fb2")}
    return file_list


change_dir()
print(fb2_file_search())
print(incorrect_file_search())
