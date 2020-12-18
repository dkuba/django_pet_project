import time

import pytest
from selenium.webdriver.common.keys import Keys


def check_for_row_in_list_table(table, row_text):
    """подтверждение строки в таблице списка"""
    rows = table.find_elements_by_tag_name('tr')
    assert row_text in [row.text for row in rows]


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
    input_box.send_keys(Keys.ENTER)
    time.sleep(1)

    check_for_row_in_list_table(ui_browser.find_element_by_id('id_list_table'), '1: Купить молока')

    # текстовое поле по прежнему предлагает добавить еще один элемент
    # пользователь вводит "Сварить кашу"
    input_box = ui_browser.find_element_by_id('id_new_item')
    assert input_box.get_attribute('placeholder') == 'Enter a to-do item'
    input_box.send_keys("Сварить кашу")

    # пользователь нажимает "Enter" страница обновляется и теперь содержит "2: Сварить кашу" в качестве
    # первого элемента списка
    input_box.send_keys(Keys.ENTER)
    time.sleep(1)

    check_for_row_in_list_table(ui_browser.find_element_by_id('id_list_table'), '1: Купить молока')
    check_for_row_in_list_table(ui_browser.find_element_by_id('id_list_table'), "2: Сварить кашу")

    assert "Закончить тест!"






