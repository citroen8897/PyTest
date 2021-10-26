from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrive_it_later(self):
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('список дел', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Введите задачу')
        inputbox.send_keys('Купить летнюю резину')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить летнюю резину')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Перебортировать летние колеса')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Купить летнюю резину')
        self.wait_for_row_in_list_table('2: Перебортировать летние колеса')

        self.fail('Закончить тест!')

    def test_start_a_list_for_one_user(self):
        self.wait_for_row_in_list_table('1: Купить летнюю резину')
        self.wait_for_row_in_list_table('2: Перебортировать летние колеса')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить летнюю резину')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить летнюю резину')

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить летнюю резину', page_text)
        self.assertNotIn('Перебортировать летние колеса', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить продукты')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить продукты')

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить летнюю резину', page_text)
        self.assertIn('Купить продукты', page_text)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
