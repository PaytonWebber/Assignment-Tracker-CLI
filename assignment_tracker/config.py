# config.py

import configparser
from rich import print
from rich.prompt import Prompt
import pkg_resources

#config_path = pkg_resources.resource_filename('assignment_tracker', 'config.ini')
config_path = 'config.ini'

# Load the configuration from config.ini
config = configparser.ConfigParser()
config.read(config_path)


try:
    CSV_FILE = config['PATHS']['csv_file']
except KeyError:
    CSV_FILE = Prompt.ask('[bold blue]Please enter the path to your CSV file[/bold blue]')
    # Ensure the PATHS section exists
    if not config.has_section('PATHS'):
        config.add_section('PATHS')
    config.set('PATHS', 'csv_file', CSV_FILE)
    with open(config_path, 'w') as f:
        config.write(f)
    CSV_FILE = config['PATHS']['csv_file']


try:
    DAYS_NOTICE = int(config['Notice']['days_notice'])
except KeyError:
    # Check if the Notice section exists
    if not config.has_section('Notice'):
        config.add_section('Notice')
        DAYS_NOTICE = Prompt.ask('[bold blue]Please enter the number of days notice you would like to receive[/bold blue]')
        config['Notice']['days_notice'] = str(DAYS_NOTICE)
        with open(config_path, 'w') as f:
            config.write(f)
    DAYS_NOTICE = int(config['Notice']['days_notice'])

try:
    CLASSES = [class_name for class_name in config['Classes'].values()]
except KeyError:
    # Check if the CLASSES section exists
    if not config.has_section('Classes'):
        config.add_section('Classes')
        with open(config_path, 'w') as f:
            config.write(f)
    CLASSES = [class_name for class_name in config['Classes'].values()]

try:
    ASSIGNMENTS = [(assignment_name, class_name) for assignment_name, class_name in zip(config['Assignments'].values(), config['Assignments'].keys())]
except KeyError:
    # Check if the ASSIGNMENTS section exists
    if not config.has_section('Assignments'):
        config.add_section('Assignments')
    ASSIGNMENTS = [(assignment_name, class_name) for assignment_name, class_name in zip(config['Assignments'].values(), config['Assignments'].keys())]