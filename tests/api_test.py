import pytest, json

from app import app

def test_get_api_posts():

    resp = app.test_client().get('/api/posts')
    data = json.loads(resp.data)
    # print(type(data))
    # print(data[0])
    assert resp.status_code == 200
    assert isinstance(data, list), "Возвращен не список"
    assert 'poster_name' in data[0], "Нет нужного ключа"  # можно проверить на остальные, но смысла нет

def test_get_api_post():

    resp = app.test_client().get('/api/posts/1')
    data = json.loads(resp.data)
    assert resp.status_code == 200
    assert isinstance(data, dict), "Возвращен не словарь"
    assert 'poster_name' in data, "В словаре нет нужного ключа"