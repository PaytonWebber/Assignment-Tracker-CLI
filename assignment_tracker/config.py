# config.py

import configparser

# Load the configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

try:
    CSV_FILE = config['General']['CSV_FILE']
    DAYS_NOTICE = int(config['General']['DAYS_NOTICE'])
except KeyError:
    print("Error: config.ini is missing required fields. Please check the README for more information.")
    exit(1)

# Check if the config has classes and assignments
if 'Classes' not in config or 'Assignments' not in config:
    print("Error: config.ini is missing required fields. Please check the README for more information.")
    exit(1)

CLASSES = [class_name for class_name in config['Classes'].values()]
ASSIGNMENTS = [(assignment_name, class_name) for assignment_name, class_name in zip(config['Assignments'].values(), config['Assignments'].keys())]