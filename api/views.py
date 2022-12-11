import json
from flask import Blueprint
from posts.dao.posts_dao import PostsDAO
from log.api import logger_api
api_bp = Blueprint(
    'api_bp', __name__,
    url_prefix='/api'
)

posts = PostsDAO()

@api_bp.route('/posts', methods=["GET"])
def index():
    logger_api.info('Запрос /api/posts')
    return json.dumps(posts.get_all(), ensure_ascii=False)

@api_bp.route('/posts/<int:pk>', methods=["GET"])
def post_by_pk(pk):
    logger_api.info(f"Запрос /api/posts/{pk}")
    return json.dumps(posts.get_by_pk(pk), ensure_ascii=False)