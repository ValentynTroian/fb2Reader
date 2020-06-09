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


change_dir()
fb2_file_search()
for fb2_file in fb2_file_search():
    tree = ET.parse(fb2_file)
    root = tree.getroot()
#    for child in root:
#        print (child.tag, child.attrib)
    for child in root:
        #print(child.tag, child.attrib)
        """
        for child2 in child:
            print(child2.tag, child2.attrib)
            for child3 in child2:
                print(child3.text, child3.text)
                """
    #print(root.tag)
    for neighbor in root.iter('{http://www.gribuser.ru/xml/fictionbook/2.0}book-title'):
        print(neighbor.text)
        #print(1)

"""
try:
  print(x)
except:
  print("An exception occurred")
"""


