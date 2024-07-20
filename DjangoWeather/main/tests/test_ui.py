from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class UITest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_search_city(self):
        self.browser.get(self.live_server_url)
        city_input = self.browser.find_element(By.ID, 'cityInput')
        city_input.send_keys('Москва')
        city_input.send_keys(Keys.RETURN)
        self.assertIn('Москва', self.browser.page_source)

    def test_city_suggestions(self):
        self.browser.get(self.live_server_url)
        city_input = self.browser.find_element(By.ID, 'cityInput')
        city_input.send_keys('Москва')
        self.browser.implicitly_wait(2)
        suggestions = self.browser.find_elements(By.CLASS_NAME, 'suggestion-item')
        self.assertTrue(len(suggestions) > 0)
        suggestions[0].click()
        self.assertEqual(city_input.get_attribute('value'), 'Москва, Россия')
