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
        for paragraph in section.findall('{http://www.gribuser.ru/xml/fictionbook/2.0}p'):
            i = i+1
    return i


def count_words(elem_tree):
    cnt_words = 0
    for section in elem_tree.iter('{http://www.gribuser.ru/xml/fictionbook/2.0}section'):
        for paragraph in section.findall('{http://www.gribuser.ru/xml/fictionbook/2.0}p'):
            if (paragraph.text is None) or (len(paragraph.text) == 0):
                continue
            cnt_words = cnt_words + len(paragraph.text.split())
    return cnt_words


def get_book_name(elem_tree):
    book_name = ""
    for section in elem_tree.iter('{http://www.gribuser.ru/xml/fictionbook/2.0}title-info'):
        for title in section.findall('{http://www.gribuser.ru/xml/fictionbook/2.0}book-title'):
            book_name = title.text

    return book_name


def main():
    change_dir()
    fb2_file_search()
    for fb2_file in fb2_file_search():
        tree = ET.parse(fb2_file)
        paragraph_cnt = count_paragraph(tree)
        book_name = get_book_name(tree)
        word_count = count_words(tree)
        print(paragraph_cnt)
        print(book_name)
        print(word_count)


main()


"""
try:
  print(x)
except:
  print("An exception occurred")
"""


