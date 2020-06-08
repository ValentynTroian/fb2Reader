import glob, os
import shutil


def change_dir():
    os.chdir('./res')


def fb2_file_search():
    incorrect_file_removal()
    fb2_file_list = {file for file in glob.glob("*.fb2")}
    return fb2_file_list


def incorrect_file_removal():
    change_dir()
    file_list = {file for file in glob.glob("*.*") if file not in glob.glob("*.fb2")}
    if not os.path.exists('incorrect_input'):
        os.makedirs('incorrect_input')
    for f in file_list:
        shutil.move(f, 'incorrect_input')


fb2_file_search()

try:
  print(x)
except:
  print("An exception occurred")


