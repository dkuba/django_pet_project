import time

from selenium.webdriver.common.keys import Keys


def test_new_visitor(ui_browser):
    """тест: начать список и получить позже"""

    # пользователь открывает страницу
    ui_browser.get('http://localhost:8000')

    # заголовок и шапка страницы говорят о том что это приложение - список неотложных дел
    assert 'To-Do' in ui_browser.title

    header_text = ui_browser.find_element_by_tag_name('h1').text
    assert 'To-Do' in header_text

    # пользователю предлагается ввести элемент списка
    input_box = ui_browser.find_element_by_id('id_new_item')
    assert input_box.get_attribute('placeholder') == 'Enter a to-do item'

    # пользователь набирает в текстовом поле "Купить молока"
    input_box.send_keys("Купить молока")

    # пользователь нажимает "Enter" страница обновляется и теперь содержит "1: Купить молока" в качестве
    # первого элемента списка
    input_box.send_keys(Keys.ENTERqq)
    time.sleep(1)

    table = ui_browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    assert any(row.text == "1: Купить молока" for row in rows)

    # текстовое поле по прежнему предлагает добавить еще один элемент
    # пользователь вводит "Сварить кашу"

    assert not "Закончить тест!"






