import glob
import os
import shutil
import xml.etree.ElementTree as ET


def change_dir():
    os.chdir('./res')


def fb2_file_search():
    incorrect_file_removal()
    fb2_file_list = {file for file in glob.glob("*.fb2")}
    return fb2_file_list


def incorrect_file_removal():
    file_list = {file for file in glob.glob("*.*") if file not in glob.glob("*.fb2")}
    if not os.path.exists('incorrect_input'):
        os.makedirs('incorrect_input')
    for f in file_list:
        shutil.move(f, 'incorrect_input')


def count_paragraph(elem_tree):
    i = 0
    for section in elem_tree.iter('{http://www.gribuser.ru/xml/fictionbook/2.0}section'):
        for _ in section.findall('{http://www.gribuser.ru/xml/fictionbook/2.0}p'):
            i = i+1
    print(i)
    return i


change_dir()
fb2_file_search()
for fb2_file in fb2_file_search():
    tree = ET.parse(fb2_file)
    root = tree.getroot()
    count_paragraph(tree)




"""
try:
  print(x)
except:
  print("An exception occurred")
"""


