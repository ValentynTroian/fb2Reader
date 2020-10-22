import glob
import os
import shutil
import xml.etree.ElementTree as ET
import logging
from loguru import logger
import collections
import re


# Class stores file info before it is loaded to the database
class FileInfo:

    def __init__(self, book_name, number_of_paragraph, number_of_words, number_of_letters
                 , words_with_capital_letters, words_in_lowercase):
        logger.info('FileInfo object is created')
        self.book_name = book_name
        self.number_of_paragraph = number_of_paragraph
        self.number_of_words = number_of_words
        self.number_of_letters = number_of_letters
        self.words_with_capital_letters = words_with_capital_letters
        self.words_in_lowercase = words_in_lowercase

    @logger.catch()
    def print(self):
        print('Book name:', self.book_name)
        print('Number of paragraphs:', self.number_of_paragraph)
        print('Number of words:', self.number_of_words)
        print('Number of letters:', self.number_of_letters)
        print('Number of words with capital letters:', self.words_with_capital_letters)
        print('Number of words in lowercase:', self.words_in_lowercase)


# Class provides functionality to search for fb2 files
class Fb2Reader:

    def __init__(self):
        logger.info('Fb2Reader object is created')

    @logger.catch()
    def fb2_file_search(self):
        os.chdir('./res/input')
        self.__incorrect_file_removal()
        fb2_file_list = {file for file in glob.glob("*.fb2")}
        logger.info('File search is done')
        return fb2_file_list

    @logger.catch()
    def parse_fb2(self, fb2_file):
        tree = ET.parse(fb2_file)
        logger.info('File is parsed')
        return tree

    @logger.catch()
    def __incorrect_file_removal(self):  # private
        file_list = {file for file in glob.glob("*.*") if file not in glob.glob("*.fb2")}
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(os.path.dirname(os.getcwd()))
        if not os.path.exists('./incorrect_input'):
            os.makedirs('./incorrect_input')
        os.path.dirname(os.getcwd())
        os.chdir('./input')
        for f in file_list:
            shutil.move(f, os.path.dirname(os.getcwd()) + '\\incorrect_input')
            logger.debug(f + ' is moved to the incorrect_input folder')
        logger.info('Incorrect files are removed')


# Class provides functionality to analyse fb2 files
class FileService:

    def __init__(self):
        logger.info('FileService object is created')

    @logger.catch()
    def count_paragraph(self, elem_tree):
        cnt_par = 0
        for section in elem_tree.iter('{http://www.gribuser.ru/xml/fictionbook/2.0}section'):
            for paragraph in section.findall('{http://www.gribuser.ru/xml/fictionbook/2.0}p'):
                cnt_par += 1
        logger.info('Number of paragraphs is calculated')
        logger.debug('Number of paragraphs: ' + str(cnt_par))
        return cnt_par

    @logger.catch()
    def count_words(self, elem_tree):
        cnt_words = 0
        for section in elem_tree.iter('{http://www.gribuser.ru/xml/fictionbook/2.0}section'):
            for paragraph in section.findall('{http://www.gribuser.ru/xml/fictionbook/2.0}p'):
                if (paragraph.text is None) or (len(paragraph.text) == 0):
                    continue
                cnt_words += len(paragraph.text.split())
        logger.info('Number of words is calculated')
        logger.debug('Number of words: ' + str(cnt_words))
        return cnt_words

    @logger.catch()
    def count_letters(self, elem_tree):
        cnt_letters = 0
        for section in elem_tree.iter('{http://www.gribuser.ru/xml/fictionbook/2.0}section'):
            for paragraph in section.findall('{http://www.gribuser.ru/xml/fictionbook/2.0}p'):
                if (paragraph.text is None) or (len(paragraph.text) == 0):
                    continue
                for word in paragraph.text.split():
                    cnt_letters += len(word)
        logger.info('Number of letters is calculated')
        logger.debug('Number of letters: ' + str(cnt_letters))
        return cnt_letters

    @logger.catch()
    def count_words_with_capital_letters(self, elem_tree):
        cnt_cap_letters = 0
        for section in elem_tree.iter('{http://www.gribuser.ru/xml/fictionbook/2.0}section'):
            for paragraph in section.findall('{http://www.gribuser.ru/xml/fictionbook/2.0}p'):
                if (paragraph.text is None) or (len(paragraph.text) == 0):
                    continue
                for word in paragraph.text.split():
                    if word == word.capitalize():
                        cnt_cap_letters += 1
        logger.info('Number of words with capital letter is calculated')
        logger.debug('Number of words with capital letter : ' + str(cnt_cap_letters))
        return cnt_cap_letters

    @logger.catch()
    def count_words_with_lowercase_letters(self, elem_tree):
        cnt_low_letters = 0
        for section in elem_tree.iter('{http://www.gribuser.ru/xml/fictionbook/2.0}section'):
            for paragraph in section.findall('{http://www.gribuser.ru/xml/fictionbook/2.0}p'):
                if (paragraph.text is None) or (len(paragraph.text) == 0):
                    continue
                for word in paragraph.text.split():
                    if word.islower():
                        cnt_low_letters += 1
        logger.info('Number of words in lowercase is calculated')
        logger.debug('Number of words lowercase : ' + str(cnt_low_letters))
        return cnt_low_letters

    @logger.catch()
    def get_book_name(self, elem_tree):
        book_name = ""
        for section in elem_tree.iter('{http://www.gribuser.ru/xml/fictionbook/2.0}title-info'):
            for title in section.findall('{http://www.gribuser.ru/xml/fictionbook/2.0}book-title'):
                book_name = title.text
        logger.info('Book name is extracted')
        logger.debug('Book name is : ' + book_name)
        return book_name

    @logger.catch()
    def word_frequency(self, elem_tree):
        word_list_full = []
        all_words_frequency_dict = collections.Counter()
        capitalized_words_dict = collections.Counter()
        for section in elem_tree.iter('{http://www.gribuser.ru/xml/fictionbook/2.0}section'):
            for paragraph in section.findall('{http://www.gribuser.ru/xml/fictionbook/2.0}p'):
                if (paragraph.text is None) or (len(paragraph.text) == 0):
                    continue
                word_list_full += paragraph.text.split()
        word_list_full = [re.sub(r'[^\w\s]', '', item) for item in word_list_full]
        for word_all in word_list_full:
            if word_all.lower() != '':
                all_words_frequency_dict[word_all.lower()] += 1
        for word_cap in word_list_full:
            if word_cap.capitalize() == word_cap:
                if word_cap.lower() != '':
                    capitalized_words_dict[word_cap.lower()] += 1
        word_dict_combined = {key: [all_words_frequency_dict[key.lower()],
                                    capitalized_words_dict[key.lower()]] for key in all_words_frequency_dict}
        logger.info('Word frequency is calculated')
        return word_dict_combined


# Class provides functionality to load fb2 file information to the database.
class DBWriter:

    def __init__(self):
        logger.info('DBWriter object is created')


@logger.catch()
def main():
    logger.add('debug.log', format="{time} {level} {message}", level="DEBUG", rotation="1 day", compression="zip")
    logger.info('------------------------------------')
    logger.info('Application started')
    logger.info('------------------------------------')

    search = Fb2Reader()
    for fb2_file in search.fb2_file_search():
        tree = search.parse_fb2(fb2_file)
        file_service = FileService()
        # get all attributes
        book_name = str(file_service.get_book_name(tree))
        paragraph_cnt = str(file_service.count_paragraph(tree))
        word_count = str(file_service.count_words(tree))
        letters_count = str(file_service.count_letters(tree))
        words_with_capital_letter = str(file_service.count_words_with_capital_letters(tree))
        words_with_lowercase_letter = str(file_service.count_words_with_lowercase_letters(tree))
        book = FileInfo(book_name, paragraph_cnt, word_count, letters_count, words_with_capital_letter
                        , words_with_lowercase_letter)
        book.print()
        file_service.word_frequency(tree)
    logger.info('------------------------------------')
    logger.info('Application ended')
    logger.info('------------------------------------')

main()
