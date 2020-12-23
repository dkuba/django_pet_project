import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    """тест нового посетителя"""

    def setUp(self) -> None:
        """установка"""
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        """демонтаж"""
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """ожидать строку в таблице списка"""
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = self.browser.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def check_for_row_in_list_table(self, row_text):
        """подтверждение строки в таблице списка"""
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        assert row_text in [row.text for row in rows]

    def test_can_start_a_list_for_one_user(self):
        """тест: начать список для одного пользователя и получить список на экране"""

        # пользователь открывает страницу
        self.browser.get(self.live_server_url)

        # заголовок и шапка страницы говорят о том что это приложение - список неотложных дел
        assert 'To-Do' in self.browser.title

        header_text = self.browser.find_element_by_tag_name('h1').text
        assert 'To-Do' in header_text

        # пользователю предлагается ввести элемент списка
        input_box = self.browser.find_element_by_id('id_new_item')
        assert input_box.get_attribute('placeholder') == 'Enter a to-do item'

        # пользователь набирает в текстовом поле "Купить молока"
        input_box.send_keys("Купить молока")

        # пользователь нажимает "Enter" страница обновляется и теперь содержит "1: Купить молока" в качестве
        # первого элемента списка
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молока')

        # текстовое поле по прежнему предлагает добавить еще один элемент
        # пользователь вводит "Сварить кашу"
        input_box = self.browser.find_element_by_id('id_new_item')
        assert input_box.get_attribute('placeholder') == 'Enter a to-do item'
        input_box.send_keys("Сварить кашу")

        # пользователь нажимает "Enter" страница обновляется и теперь содержит "2: Сварить кашу" в качестве
        # первого элемента списка
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Купить молока')
        self.wait_for_row_in_list_table("2: Сварить кашу")

        assert "Закончить тест!"

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """тест: многочисленные пользователи могут начать список по разным url"""

        # Пользователь1 начинает новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить молока')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Купить молока')

        # Пользователь1 замечает что список имеет уникальный url адрес
        user_one_list_url = self.browser.current_url
        self.assertRegex(user_one_list_url, '/lists/.+')

        # Пользователь2 приходит на сайт

        ## используем новый сеанс браузера для чистоты теста
        
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Пользователь2 посещает домашнюю страницу. Нет признаков списка Пользователя1
        
        self.browser.get(self.live_server_url)
        
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить молока', page_text)
        
        # Пользователь2 начинает новый список
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить хлеб')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить хлеб')
        
        # Пользователь2 получает уникальный URL-адрес
        user_two_list_url = self.browser.current_url
        self.assertRegex(user_two_list_url, '/list/.+')
        self.assertNotEqual(user_two_list_url, user_one_list_url)
        
        # нет следов списка Пользователя2
        page_text = self.browser.find_elements_by_tag_name('body').text
        self.assertNotIn('Купить молока', page_text)
        self.assertIn('Купить хлеб', page_text)

        # конец
