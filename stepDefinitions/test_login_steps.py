import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from pages.login_page import Login_Page
from pages.inventory_page import InventoryPage # Ensure you created this
import time

scenarios('../features/login.feature')

@given('the user is logged into SauceDemo')
def login_user(driver):
    driver.get("https://saucedemo.com")
    login = Login_Page(driver)
    login.login("standard_user", "secret_sauce")

@when(parsers.parse('the user sorts products by "{sort_option}"'))
def sort_products(driver, sort_option):
    inventory = InventoryPage(driver)
    inventory.sort_products(sort_option)

@then(parsers.parse('the first product should be "{expected_name}"'))
def verify_sort(driver, expected_name):
    inventory = InventoryPage(driver)
    actual_name = inventory.get_first_product_name()
    assert actual_name == expected_name

@when('the user clicks on the Twitter icon')
def click_twitter(driver, context):
    context['parent_handle'] = driver.current_window_handle
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element("link text", "Twitter").click()
    time.sleep(2) # Brief wait for window to spawn

@then('a new window should open with Twitter')
def verify_window(driver, context):
    all_handles = driver.window_handles
    for handle in all_handles:
        if handle != context['parent_handle']:
            driver.switch_to.window(handle)
            break
    
    assert "twitter.com" in driver.current_url.lower() or "x.com" in driver.current_url.lower()
    driver.close()
    driver.switch_to.window(context['parent_handle'])