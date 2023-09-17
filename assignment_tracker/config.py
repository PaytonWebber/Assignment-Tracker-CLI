# config.py

import configparser
from rich.prompt import Prompt
import pkg_resources

config_path = pkg_resources.resource_filename('assignment_tracker_cli', 'config.ini')

# Load the configuration from config.ini
config = configparser.ConfigParser()
config.read(config_path)

try:
    CSV_FILE = config['General']['CSV_FILE']
except KeyError:
    CSV_FILE = Prompt.ask('[bold blue]Please enter the path to your CSV file[/bold blue]')
    config['General']['CSV_FILE'] = CSV_FILE
    with open('config.ini', 'w') as f:
        config.write(f)

try:
    DAYS_NOTICE = int(config['General']['DAYS_NOTICE'])
except KeyError:
    DAYS_NOTICE = Prompt.ask('[bold blue]Please enter the number of days notice you would like to receive[/bold blue]')
    config['General']['DAYS_NOTICE'] = str(DAYS_NOTICE)
    with open('config.ini', 'w') as f:
        config.write(f)
    
CLASSES = [class_name for class_name in config['Classes'].values()]
ASSIGNMENTS = [(assignment_name, class_name) for assignment_name, class_name in zip(config['Assignments'].values(), config['Assignments'].keys())]