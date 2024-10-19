import time
from Pages.BasePage import BasePage
from Pages.LoginPage import LoginPage
from Utilities.CustomLogger import LogGen
from Utilities.ConfigReader import read_config as rc

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException

import sys


def test_application_login_with_valid_data(setup):
    driver = setup
    bp = BasePage(driver)
    lp = LoginPage(driver)
    log = bp.log
    wait = WebDriverWait(driver, 10)
    err_count = 0

    log.info("---- LOGIN APPLICATION WITH VALID DATA TEST BEGINS -----")
    username = rc('COMMON_INFO', 'user_name')
    password = rc('COMMON_INFO', 'password')
    expected = rc('COMMON_INFO', "dashboard_url")
    
    lp.login_application(username, password)
    try:
        # waiting for dashboard to be displayed
        wait.until(EC.url_to_be(expected))
        time.sleep(2)
        text = driver.find_element(By.XPATH, "//body").text

        # checking dashboard navigation by verifying text presence in dashboard
        if any(i not in text for i in ("Time at Work", "Quick Launch")):
            log.error("Failing to login and navigate to dashboard")
            err_count += 1
    except TimeoutException:
        log.error("Failing to login and navigate to dashboard")
        err_count += 1
    
    if err_count != 0:
        sys.exit()
    
    log.info("---- LOGIN APPLICATION WITH VALID DATA TEST COMPLETE -----")

def test_application_login_with_invalid_data(setup):
    driver = setup
    bp = BasePage(driver)
    lp = LoginPage(driver)
    log = bp.log
    wait = WebDriverWait(driver, 10)
    err_count = 0

    log.info("---- LOGIN APPLICATION WITH INVALID DATA TEST BEGINS -----")
    def validate_err_msg():
        nonlocal err_count
        err_msg_xpath = rc(lp.section, "invalid_credentials_err_msg_container_xpath")
        try:
            # waiting for error message container display
            wait.until(EC.visibility_of_element_located((By.XPATH, err_msg_xpath)))
            actual_err_msg = bp.get_element(lp.section, "invalid_credentials_err_msg_container_xpath").text
            expected_err_msg = "Invalid credentials"
            if actual_err_msg != expected_err_msg:
                log.error(f"Expected err msg '{expected_err_msg}' but actual '{actual_err_msg}'")
                err_count += 1
        except TimeoutException:
            log.error("Failed to display error message on entering invalid credentials")
            err_count += 1
        return err_count

    log.info("---- LOGIN WITH VALID USERNAME AND INVALID PASSWORD ----")
    username = rc('COMMON_INFO', 'user_name')
    password = bp.random_alphanum_strig_generator(8)
    
    lp.login_application(username, password)
    err_count += validate_err_msg()
    
    log.info("---- LOGIN WITH INVALID USERNAME AND VALID PASSWORD ----")
    username = bp.random_alphanum_strig_generator(8)
    password = rc('COMMON_INFO', 'password')
    
    lp.login_application(username, password)
    err_count += validate_err_msg()
    
    log.info("---- LOGIN WITH INVALID USERNAME AND INVALID PASSWORD ----")
    username = bp.random_alphanum_strig_generator(8)
    password = bp.random_alphanum_strig_generator(8)
    
    lp.login_application(username, password)
    err_count += validate_err_msg()

    if err_count != 0:
        sys.exit()
    
    log.info("---- LOGIN APPLICATION WITH INVALID DATA TEST COMPLETE -----")