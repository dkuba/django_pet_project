from django.template.loader import render_to_string
from django.urls import resolve
from django.http import HttpRequest
from pytest_django.fixtures import client

from lists.views import home_page


def test_root_url_resolves_to_home_page_view():
    """корневой url преобразуется в представление домашней страницы"""
    found = resolve('/')
    assert found.func == home_page


def test_home_page_returns_correct_html(client):
    """тест: домашняя страница возвращает правильный html"""
    request = HttpRequest()
    response = client.get('/')
    html = response.content.decode('utf8')
    expected_html = render_to_string('home.html')
    assert html == expected_html
