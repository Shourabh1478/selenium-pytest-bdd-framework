from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InventoryPage(BasePage):
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")

    def sort_products(self, sort_option):
        self.select_from_dropdown(self.SORT_DROPDOWN, sort_option)

    def get_first_product_name(self):
        return self.find_element(self.PRODUCT_NAMES).text