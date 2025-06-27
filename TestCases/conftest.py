import time
import pytest
from selenium import webdriver

import subprocess

from PageObjects.BasePage import BasePage as bp
from Utilities.ConfigReader import read_config as rc
from db_obj import dbobj as db

# This checks virtual environment presence in project before session starts
def pytest_sessionstart(session):
    bp.check_virtual_environment()
    subprocess.run("pip install -r requirements.txt", shell=True)  # This installs all dependencies listed in requirements.txt file

# BASE METHOD TO INTIATE WEBDRIVER, LAUNCH BASE PAGE, AND TEARDOWN METHODS
@pytest.fixture(scope="class")
def setup():
    chrome_options = webdriver.ChromeOptions()
    firefox_options = webdriver.FirefoxOptions()
    edge_options = webdriver.EdgeOptions()
    safari_options = webdriver.SafariOptions()

    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(2)
    driver.get(rc('COMMON_INFO', 'base_url'))
    driver.maximize_window()
    driver.implicitly_wait(20)

    yield driver
    driver.quit()
    db.conn.close()
