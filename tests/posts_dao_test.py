import pytest
from posts.dao.posts_dao import PostsDAO


# Нам пригодится экземпляр DAO, так что мы создадим его в фикстуре
# Но пригодится только один раз, поэтому выносить в conftest не будем
@pytest.fixture()
def posts_dao():
    posts_dao_instance = PostsDAO()
    return posts_dao_instance

keys_should_be = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}

class TestPostsDao:

    def test_get_all(self, posts_dao):
        """ Проверяем, верный ли список постов возвращается """
        posts = posts_dao.get_all()
        assert type(posts) == list, "возвращается не список"
        assert len(posts) > 0, "возвращается пустой список"
        assert set(posts[0].keys()) == keys_should_be, "неверный список ключей"

    def test_get_by_pk(self, posts_dao):
        """ Проверяем, верный ли пост возвращается при запросе одного """
        post = posts_dao.get_by_pk(1)
        assert post["pk"] == 1, "возвращается неправильный пост"
        assert set(post.keys()) == keys_should_be, "неверный список ключей"

    def test_get_by_user(self, posts_dao):
        """ Проверяем, верный ли список постов возвращается при запросе постов по юзернейму"""
        posts = posts_dao.get_by_user('leo')
        assert type(posts) == list, "возвращается не список"
        assert len(posts) > 0, "возвращается пустой список"
        assert set(posts[0].keys()) == keys_should_be, "неверный список ключей"
        with pytest.raises(ValueError):
            posts_dao.get_by_user('alex')

    def test_search_by_keyword(self, posts_dao):
        """ Проверяем, возвращает ли посты по ключевому слову"""
        posts = posts_dao.search_by_keyword('кот')
        assert type(posts) == list, "возвращается не список"
        assert len(posts) > 3, "не находит все вхождения 'кот'" # в дефолтном posts.json 4 поста с вхождением "кот"
        assert set(posts[0].keys()) == keys_should_be, "неверный список ключей"
        posts = posts_dao.search_by_keyword('который')
        assert len(posts) == 0, "возвращается НЕ пустой список"  # в дефолтном posts.json нет вхождений "который"