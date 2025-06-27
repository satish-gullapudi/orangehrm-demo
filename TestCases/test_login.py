import time
from datetime import datetime

from PageObjects.BasePage import BasePage
from PageObjects.LoginPage import LoginPage
from TestCases.conftest import setup
from Utilities.CustomLogger import LogGen
from Utilities.ConfigReader import read_config as rc

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from db_obj import dbobj as db

import sys


def test_application_login_with_valid_data(setup):
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
    try:
        lp.login_application(username, password)
        # waiting for dashboard to be displayed
        wait.until(EC.url_to_be(expected))
        time.sleep(2)
        text = driver.find_element(By.XPATH, "//body").text

        # checking dashboard navigation by verifying text presence in dashboard
        if any(i not in text for i in ("Time at Work", "Quick Launch")):
            bp.log.error("Failing to login and navigate to dashboard")
            err_count += 1
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if err_count == 0:
            db.log_test_result("Login Test", "Login", "PASS", start_time, end_time)
    except Exception or err_count != 0:
        bp.log.error("Failing to login and navigate to dashboard")
        db.log_test_result("Login Test", "Login", "FAIL", start_time, end_time, error_message=str(Exception),
                           screenshot_path="screenshots/login_fail.png")

    bp.log.info("---- LOGIN APPLICATION WITH VALID DATA TEST COMPLETE -----")

def test_application_login_with_invalid_data(setup):
    driver = setup
    bp = BasePage(driver)
    lp = LoginPage(driver)
    log = bp.log
    wait = WebDriverWait(driver, 10)
    err_count = 0
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
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

        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if err_count == 0:
            db.log_test_result("Login Test Invalid Data", "Login", "PASS", start_time, end_time)
    except Exception or err_count != 0:
        bp.log.error("Failing to login and navigate to dashboard")
        db.log_test_result("Login Test Invalid Data", "Login", "FAIL", start_time, end_time, error_message=str(Exception),
                           screenshot_path="screenshots/login_fail.png")

    log.info("---- LOGIN APPLICATION WITH INVALID DATA TEST COMPLETE -----")

def test_login_page_footer_links(setup):
    driver = setup
    bp = BasePage(driver)
    lp = LoginPage(driver)
    log = bp.log
    wait = WebDriverWait(driver, 10)
    err_count = 0
    main_window = driver.current_window_handle
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        log.info("---- FOOTER LINKS TEST BEGINS -----")
        def validate_footer_links(xpath, expected):
            nonlocal err_count
            ele = rc(lp.section, xpath)
            wait.until(EC.element_to_be_clickable((By.XPATH, ele)))
            handles = driver.window_handles
            bp.click_element(lp.section, xpath)
            wait.until(EC.new_window_is_opened(handles))
            handles = driver.window_handles
            new_window = handles[1]
            driver.switch_to.window(new_window)
            actual = driver.current_url

            if actual != expected:
                log.error(f"Expected to launch '{expected}' in new window but actual '{actual}'")
                err_count += 1
            driver.close()
            driver.switch_to.window(main_window)
            return err_count

        err_count += validate_footer_links("footer_links_linkedin_xpath", "https://www.linkedin.com/company/orangehrm")
        err_count += validate_footer_links("footer_links_facebook_xpath", "https://www.facebook.com/OrangeHRM/")
        err_count += validate_footer_links("footer_links_twitter_xpath", "https://x.com/orangehrm?lang=en")
        err_count += validate_footer_links("footer_links_youtube_xpath", "https://www.youtube.com/c/OrangeHRMInc")
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if err_count == 0:
            db.log_test_result("Login Test Invalid Data", "Login", "PASS", start_time, end_time)

    except Exception or err_count != 0:
        bp.log.error("Failing to login and navigate to dashboard")
        db.log_test_result("Login Test Invalid Data", "Login", "FAIL", start_time, end_time, error_message=str(Exception),
                           screenshot_path="screenshots/login_fail.png")
    log.info("---- FOOTER LINKS TEST COMPLETE -----")