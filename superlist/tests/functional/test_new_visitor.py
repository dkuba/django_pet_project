import pytest


@pytest.mark.skip(reason="Сейчас не нужны UI тесты")
def test_new_visitor(ui_browser):

    # Здесь описание тест-кейса как он есть

    assert 'To-Do' in ui_browser.title

    # Дейсвтие 1
    # Дейсвтие 2
    # ...
    # Дейсвтие n





