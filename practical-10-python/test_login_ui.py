"""Selenium UI tests for the local demonstration login page."""

import unittest
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By


LOGIN_PAGE = Path(__file__).with_name("login.html").resolve().as_uri()


class LoginUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get(LOGIN_PAGE)
        self.email = self.driver.find_element(By.ID, "email")
        self.password = self.driver.find_element(By.ID, "password")
        self.submit = self.driver.find_element(By.ID, "sign-in")
        self.message = self.driver.find_element(By.ID, "message")

    def test_valid_credentials_show_welcome(self):
        self.email.send_keys("ada@example.com")
        self.password.send_keys("LibraryDemo42")
        self.submit.click()

        self.assertEqual(self.message.text, "Welcome, Ada!")
        self.assertEqual(self.message.get_attribute("data-result"), "success")

    def test_wrong_password_shows_error(self):
        self.email.send_keys("ada@example.com")
        self.password.send_keys("wrong-password")
        self.submit.click()

        self.assertEqual(self.message.text, "Invalid email or password.")
        self.assertEqual(self.message.get_attribute("data-result"), "error")

    def test_unknown_email_shows_error(self):
        self.email.send_keys("unknown@example.com")
        self.password.send_keys("LibraryDemo42")
        self.submit.click()

        self.assertEqual(self.message.text, "Invalid email or password.")
        self.assertEqual(self.message.get_attribute("data-result"), "error")

    def test_required_fields_block_empty_submission(self):
        self.submit.click()

        validity = self.driver.execute_script(
            "return [arguments[0].validity.valueMissing, "
            "arguments[1].validity.valueMissing];",
            self.email,
            self.password,
        )
        self.assertEqual(validity, [True, True])
        self.assertEqual(self.message.text, "")

    def test_malformed_email_is_rejected_by_browser_validation(self):
        self.email.send_keys("not-an-email")
        self.password.send_keys("LibraryDemo42")
        self.submit.click()

        type_mismatch = self.driver.execute_script(
            "return arguments[0].validity.typeMismatch;", self.email
        )
        self.assertTrue(type_mismatch)
        self.assertEqual(self.message.text, "")


if __name__ == "__main__":
    unittest.main()
