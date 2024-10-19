import logging
import logging.handlers
import os
import datetime

def LogGen():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s')

    # console handler to display logs in terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    log_dir = "Logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file_name = os.path.join(log_dir, f"test_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log")

    # log file handler to genate log file in project folder
    file_handler = logging.FileHandler(log_file_name, mode='a')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # adding both handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger