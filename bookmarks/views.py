from flask import Blueprint, render_template, json, redirect
from werkzeug.exceptions import HTTPException

from bookmarks.dao import BookmarksDAO
from posts.dao.posts_dao import PostsDAO

bookmarks_bp = Blueprint(
    'bookmarks_bp', __name__,
    url_prefix='/bookmarks',
    template_folder='/main/templates'
)
posts = PostsDAO()
bookmarks = BookmarksDAO()

@bookmarks_bp.errorhandler(HTTPException)
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

@bookmarks_bp.route('/', methods=["GET"])
def bookmarks_index():
    """Выводим все закладки"""
    all_posts = posts.get_all()
    all_bookmarks = bookmarks.get_all()
    bookmarked_posts = list()
    for post in all_posts:
        if post['pk'] in all_bookmarks:
            bookmarked_posts.append(post)
    return render_template("index.html", title = 'SKYPROGRAM', posts = bookmarked_posts, bookmarks_amount = len(all_bookmarks))

@bookmarks_bp.route('/add/<int:pk>', methods=["GET"])
def add_bookmark(pk):
    """Добавляем пост в закладки"""
    bookmarks.add_bookmark(pk)
    return redirect('/', code=302)

@bookmarks_bp.route('/remove/<int:pk>', methods=["GET"])
def remove_bookmark(pk):
    """Удаляем пост из закладок"""
    bookmarks.remove_bookmark(pk)
    return redirect('/', code=302)