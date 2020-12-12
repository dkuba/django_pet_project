import pytest
from selenium import webdriver


@pytest.fixture()
def ui_browser():
    """Подключение к БД перед тестами, отключение после."""
    # Setup : start db
    browser = webdriver.Firefox()
    browser.get('http://127.0.0.1:8000')

    yield browser

    browser.quit()
