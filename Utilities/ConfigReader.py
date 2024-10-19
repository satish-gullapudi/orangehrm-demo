import configparser
import os
from pathlib import Path

# method to retrieve locator path based on pages which are divided into sections

def read_config(section, key):
    config = configparser.RawConfigParser()
    config_file_path = os.path.join(str(Path.cwd()) + '/Configurations/config.ini')
    config.read(config_file_path)
    return config.get(section, key)
