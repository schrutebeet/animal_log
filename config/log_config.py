import logging
import os
from datetime import datetime

# Create a logger
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

log_path = os.environ.get('LOGS_PATH')

# Create a file handler and set level to INFO
current_datetime = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
log_file_info = os.path.join(log_path, f'animal_INFO_{current_datetime}.txt')
log_file_debug = os.path.join(log_path, f'animal_DEBUG_{current_datetime}.txt')

file_handler_info = logging.FileHandler(log_file_info)
file_handler_debug = logging.FileHandler(log_file_debug)
file_handler_info.setLevel(logging.INFO)
file_handler_debug.setLevel(logging.DEBUG)

# Create a console handler and set level to INFO
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for both handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler_info.setFormatter(formatter)
file_handler_debug.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add both handlers to the logger
LOGGER.addHandler(file_handler_info)
LOGGER.addHandler(file_handler_debug)
LOGGER.addHandler(console_handler)
