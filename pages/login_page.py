from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class Login_Page(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")      # Was "username"
    PASSWORD_INPUT = (By.ID, "password")       # This one was actually okay
    LOGIN_BUTTON = (By.ID, "login-button")     # Was a complex CSS selector
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']") # Was "flash"

    def __init__(self, driver):
        super().__init__(driver)

    def login(self, username, password):
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def is_login_successful(self):
        return self.is_element_present(self.ERROR_MESSAGE)
