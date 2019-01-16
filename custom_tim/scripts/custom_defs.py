from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time



def login(browser,username,password):
    login_elem = browser.find_elements_by_xpath("//*[contains(text(), 'Log in')]")
    switch_acc_elem = browser.find_elements_by_xpath("//*[contains(text(), 'Switch Accounts')]")
    # if Login text is not found and no "switch accounts" option, user already logged in
    if len(login_elem) == 0 and len(switch_acc_elem) == 0:
        return True

    # Check if the first div is 'Create an Account' or 'Log In'
    login_elem = browser.find_element_by_xpath(
        "//article/div/div/p/a[text()='Log in']")
    if login_elem is not None:
        ActionChains(browser).move_to_element(login_elem).click().perform()

    time.sleep(2)

    input_username = browser.find_elements_by_xpath(
        "//input[@name='username']")

    ActionChains(browser).move_to_element(input_username[0]). \
        click().send_keys(username).perform()

    time.sleep(1)

    input_password = browser.find_elements_by_xpath(
        "//input[@name='password']")
    if not isinstance(password, str):
        password = str(password)
    ActionChains(browser).move_to_element(input_password[0]). \
        click().send_keys(password).perform()

    login_button = browser.find_element_by_xpath("//div/button[text()='Log in']")
    print 'logging in...'
    ActionChains(browser).move_to_element(login_button).click().perform()

    return True
