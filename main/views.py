from flask import Blueprint, render_template, json, request, abort
from werkzeug.exceptions import HTTPException

from bookmarks.dao import BookmarksDAO
from posts.dao.posts_dao import PostsDAO, get_comments
from json import JSONDecodeError
import logging

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates'
)


posts = PostsDAO()
bookmarks = BookmarksDAO()

@main_bp.errorhandler(HTTPException)
def handle_exception(e):
    """Ловим ошибки"""
    # получаем заголовки и код ошибки
    response = e.get_response()
    # добавляем в ответ данные
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@main_bp.route('/', methods=["GET"])
def index():
    """Выводим все посты"""
    all_posts = posts.get_all()
    all_bookmarks = bookmarks.get_all()
    print(all_bookmarks)
    return render_template("index.html", title = 'SKYPROGRAM', posts = all_posts, bookmarks_amount = len(all_bookmarks))

@main_bp.route('/user-feed/<user_name>', methods=["GET"])
def user_feed(user_name):
    """Выводим посты юзера"""
    try:
        user_posts = posts.get_by_user(user_name)
        return render_template("user-feed.html", posts = user_posts, title = 'SKYPROGRAM user feed')
    except ValueError:
        logging.error(f"Невозможно загрузить посты. Юзер {user_name} не найден")
        abort(404)

@main_bp.route('/post/<int:pk>', methods=["GET"])
def post_by_pk(pk):
    """Выводим пост по айди"""
    post = posts.get_by_pk(pk)
    post_list = post['content'].split(' ')
    fixed_post_list = []
    for word in post_list:
        if '#' in word:
            clear_tag = word.replace('#', '')
            hashtag = f"<a href=\"/tag/{clear_tag}\">{word}</a> "
            print(word, clear_tag, hashtag, sep='\n')
            fixed_post_list.append(hashtag)
        else:
            fixed_post_list.append(word)
    text_with_hashtags = ' '.join(fixed_post_list)
    comments = get_comments(pk)
    return render_template("post.html", post = post, text = text_with_hashtags, comments = comments, comments_count = len(comments), title = 'SKYPROGRAM post')

@main_bp.route('/search', methods=["GET"])
def search_post_by_keyword():
    """Выводим посты по ключевому слову"""
    s = request.args['s']
    logging.info(f'Поиск по вхождению {s}')
    try:
        founded_posts = posts.search_by_keyword(s)
        result = render_template("search.html", keyword = s, posts = founded_posts, title = 'SKYPROGRAM search')
    except FileNotFoundError:
        logging.error('JSON пропал')
        result = 'Не могу загрузить посты: файл не найден'
    except JSONDecodeError:
        logging.error('Невалидный JSON')
        result = 'Не могу загрузить посты: структура файла нарушена'
    return result

@main_bp.route('/tag/<tag>', methods=["GET"])
def search_post_by_tag(tag):
    """Выводим посты по тегу"""
    hashtag = '#' + tag
    # logging.info(f'Поиск по вхождению {s}')
    try:
        founded_posts = posts.search_by_keyword(hashtag)
        result = render_template("search.html", keyword = hashtag, posts = founded_posts, title = 'SKYPROGRAM tag')
    except FileNotFoundError:
        logging.error('JSON пропал')
        result = 'Не могу загрузить посты: файл не найден'
    except JSONDecodeError:
        logging.error('Невалидный JSON')
        result = 'Не могу загрузить посты: структура файла нарушена'
    return result