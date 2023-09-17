# utils.py

import csv
import configparser
import datetime
from rich.prompt import Confirm
from assignment_tracker import config

CLASS_LIST = [class_name for class_name in config.CLASSES]


def add_csv_path_to_config(csv_path: str):
    """ Adds a CSV path to the config file. """

    config = configparser.ConfigParser()
    config.read('config.ini')
    config['General']['CSV_FILE'] = csv_path
    with open('config.ini', 'w') as f:
        config.write(f)


def check_format(rows: list):
    """ Checks if the CSV file has the correct format. If it doesn't, it raises an error."""

    if len(rows) == 0:
        raise ValueError("Error: CSV file is empty. Please check the README for more information.\n")
    return
        

def check_csv(csv_path: str):
    """ Checks if the CSV file exists. If it doesn't, it creates it and adds the headers."""
    
    rows = []
    try:
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
            
    except FileNotFoundError:
        with open(csv_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Assignment Name', 'Class', 'Due Date', 'Status'])
            return

    try:
        check_format(rows)
        return
    except ValueError as e:
        # TODO: Add an option to overwrite the CSV file
        print(e)

        try_to_overwrite = Confirm.ask('[bold red]Would you like to overwrite the CSV file?[/bold red]')
        if try_to_overwrite:
            with open(csv_path, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['Assignment Name', 'Class', 'Due Date', 'Status'])
                return
        else:
            exit(1)


def update_config(due_soon: dict, config_path: str):
    """ Updates the config file with the data from the CSV file. The config should only have assignments due soon."""
    
    config = configparser.ConfigParser()
    config.read(config_path)
    
    # Check for the presence of 'Assignments' in the config.
    if 'Assignments' in config:
        # Remove all assignments from config
        for assignment in config['Assignments']:
            config.remove_option('Assignments', assignment)
    else:
        # If 'Assignments' section doesn't exist, create it
        config.add_section('Assignments')

    if 'Classes' not in config: config.add_section('Classes')
    for class_name in CLASS_LIST:
        config['Classes'][class_name] = class_name

    # Add assignments due soon to config
    for assignment in due_soon:
        config['Assignments'][assignment] = due_soon[assignment][1]

    with open(config_path, 'w') as f:
        config.write(f)


def get_assignments_due_soon(csv_path: str, days_notice: int) -> dict:
    #  Parse csv file
    assignments_due_soon = {}

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:

            course = row[1]
            if course not in CLASS_LIST: CLASS_LIST.append(course)


            if row[3] == 'COMPLETED' or row[2] == '': continue

            assignment_name, due_date, status = row[0], datetime.datetime.strptime(row[2], '%m/%d/%Y').date(), row[3]

            if (due_date - datetime.datetime.now().date()).days > days_notice: continue

            days_left = (due_date - datetime.datetime.now().date()).days
            assignments_due_soon[assignment_name] = (assignment_name, course, due_date, days_left, status)
    
    # Sort assignments by due date
    assignments_due_soon = dict(sorted(assignments_due_soon.items(), key=lambda item: item[1][2]))
    update_config(assignments_due_soon, 'config.ini')
    return assignments_due_soon


def update_status_value(csv_path: str, class_name: str, assignment_name: str, status: str):
    rows = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0].lower() == assignment_name.lower() and row[1] == class_name:
                row[3] = status
            rows.append(row)

    with open(csv_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def add_assignment_to_csv(csv_path: str, class_name: str, assignment_name: str, due_date: datetime.date):
    with open(csv_path, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([assignment_name, class_name, due_date, 'NOT STARTED'])


def remove_assignment_from_csv(csv_path: str, class_name: str, assignment_name: str):
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    for row in data:
        if row[0].lower() == assignment_name.lower() and row[1] == class_name:
            data.remove(row)

    with open(csv_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)
