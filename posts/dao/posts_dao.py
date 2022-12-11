import json
import logging
from bookmarks.dao import BookmarksDAO

def get_comments(post_id):
    """
    возвращает список комментариев к посту по id поста
    :param post_id:
    :return:
    """
    post_comments = list()
    try:
        with open("data/comments.json", "r", encoding='utf-8') as jsonFile:
            comments = json.load(jsonFile)
    except FileNotFoundError:
        logging.error('JSON с комментариями не найден')
    for comment in comments:
        if comment['post_id'] == post_id:
            post_comments.append(comment)
    return post_comments


class PostsDAO:

    def __init__(self):

        """
        :return:
        Возвращает посты
        """
        try:
            with open("data/posts.json", "r", encoding='utf-8') as jsonFile:
                posts = json.load(jsonFile)
        except FileNotFoundError:
            logging.error('JSON с постами не найден')

    def get_all(self):
        with open("data/posts.json", "r", encoding='utf-8') as jsonFile:
            posts = json.load(jsonFile)
        bookmarks = BookmarksDAO()
        bookmarked_posts = bookmarks.get_all()
        all_posts = []
        for post in posts:
            post['is_bookmarked'] = False
            if post['pk'] in bookmarked_posts:
                post['is_bookmarked'] = True
            all_posts.append(post)
        posts = all_posts
        return posts

    def get_by_pk(self, pk):
        """
        :param pk:
        :return:
        возвращает один пост по его идентификатору.
        """
        found_post = False
        for post in self.get_all():
            if post['pk'] == pk:
                found_post = post
        return found_post

    def get_by_user(self, user_name):
        """
        :param user_name:
        :return:
        Возвращает посты определенного пользователя.
        Функция должна вызывать ошибку `ValueError` если такого пользователя нет
        и пустой список, если у пользователя нет постов.
        """
        user_posts = list()
        for post in self.get_all():
            if post["poster_name"] == user_name:
                user_posts.append(post)
        if len(user_posts) > 0:
            return user_posts
        raise ValueError(f"Не обнаружен пользователь {user_name}")
        pass

    def search_by_keyword(self, query):
        keyword_posts = list()
        """
        возвращает список постов по ключевому слову
        :param query:
        :return:
        """
        for post in self.get_all():
            if query in post['content']:
                keyword_posts.append(post)
            if keyword_posts == 10:
                break
        return keyword_posts