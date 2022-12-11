import json
import logging

class BookmarksDAO:

    def __init__(self):

        """
        :return:
        Возвращает id постов с закладками
        """
        try:
            self.bookmarks_file = "data/bookmarks.json"
            with open(self.bookmarks_file, "r", encoding='utf-8') as jsonFile:
                bookmarks = json.load(jsonFile)
        except FileNotFoundError:
            logging.error('JSON с закладками не найден')

    def get_all(self):
        with open(self.bookmarks_file, "r", encoding='utf-8') as jsonFile:
            bookmarks = json.load(jsonFile)
        return bookmarks

    def add_bookmark(self, post_id):
        with open(self.bookmarks_file, "r", encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)
        data.append(post_id)

        with open(self.bookmarks_file, "w", encoding='utf-8') as jsonFile:
            json.dump(data, jsonFile, ensure_ascii=False)

    def remove_bookmark(self, post_id):
        with open(self.bookmarks_file, "r", encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)
        data.remove(post_id)

        with open(self.bookmarks_file, "w", encoding='utf-8') as jsonFile:
            json.dump(data, jsonFile, ensure_ascii=False)