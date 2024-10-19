import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from Utilities.ConfigReader import read_config as rc
from Utilities.CustomLogger import LogGen

import os
import sys


class BasePage:
    log = LogGen()
    
    def __init__(self, driver):
        self.driver = driver
        self.random_alphanum_strig_generator = lambda length: ''.join(random.choice(string.ascii_letters + string.digits) for char in range(length))

    @staticmethod
    def check_virtual_environment():
        # Check for common virtual environment directories
        if os.path.isdir('venv') or os.path.isdir('env') or os.path.isdir('.venv'):
            print("Virtual environment detected.")
        else:
            print("No virtual environment found.")
            print("\nIt is recommended to use a virtual environment for this project.")
            
            # Suggest creation of virtual environment
            print("\nTo create a virtual environment, follow these steps:")
            
            if sys.platform == "win32":  # Windows instructions
                print("""
        1. Open a command prompt.
        2. Run the following command to create a virtual environment:
            python -m venv venv
        3. To activate the virtual environment, run:
            venv\\Scripts\\activate.bat
        4. After activation, install the required dependencies using:
            pip install -r requirements.txt
        """)
            else:  # Linux/MacOS instructions
                print("""
        1. Open a terminal.
        2. Run the following command to create a virtual environment:
            python3 -m venv venv
        3. To activate the virtual environment, run:
            source venv/bin/activate
        4. After activation, install the required dependencies using:
            pip install -r requirements.txt
        """)
            sys.exit()
    
    def get_element(self, section, key):
        if key.endswith("xpath"):
            element = self.driver.find_element(By.XPATH, rc(section, key))
        elif key.endswith("css"):
            element = self.driver.find_element(By.CSS_SELECTOR, rc(section, key))
        elif key.endswith("id"):
            element = self.driver.find_element(By.ID, rc(section, key))
        return element

    def click_element(self, section, key):
        element = self.get_element(section, key)
        element.click()

    def type_in_field(self, section, key, data=''):
        element = self.get_element(section, key)
        element.clear()
        element.send_keys(data)

    def get_element_count_using_js(self, element_xpath):
        script = """ return document.evaluate(arguments[0], document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null).snapshotLength; """
        return self.driver.execute_script(script, element_xpath)