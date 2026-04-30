from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config_reader import ConfigReader
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, int(ConfigReader.get_config("common", "timeout")))
    
    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def click(self,locator):
        element= self.find_element(locator)
        element.click()

    def send_keys(self,locator,text):
        element= self.wait_for_clickable(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self,locator):
        element=self.find_element(locator)
        return element.text

    def is_element_present(self,locator):
        try:
            self.find_element(locator)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
        
    def wait_for_clickable(self,locator):
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def select_from_dropdown(self,locator,option_text):
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(option_text)

    def wait_for_element_to_disappear(self, locator):
        """Handles dynamic loading spinners/elements."""
        self.wait.until(EC.invisibility_of_element_located(locator))

    def switch_to_new_window(self):
        """Handles switching to new windows/tabs."""
        current_window = self.driver.current_window_handle
        all_windows = self.driver.window_handles
        for window in all_windows:
            if window != current_window:
                self.driver.switch_to.window(window)
                break

    def close_tab_and_return(self, parent_handle):
        self.driver.close()
        self.driver.switch_to.window(parent_handle)

    
    

