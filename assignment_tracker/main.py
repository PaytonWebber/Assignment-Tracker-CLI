# main.py

import datetime
import typer
from rich import print
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from assignment_tracker import config
from assignment_tracker import utils

CSV_FILE = config.CSV_FILE
DAYS_NOTICE = config.DAYS_NOTICE
CLASS_LIST = [class_name for class_name in config.CLASSES]
ASSIGNMENT_LIST = {class_name: [assignment for class_n, assignment in config.ASSIGNMENTS if class_n == class_name] for class_name in CLASS_LIST}
STATUS_LIST = ['NOT STARTED', 'IN PROGRESS', 'COMPLETED']


app = typer.Typer()
console = Console()


@app.command()
def add_csv_path(csv_path: str):
    """ Adds a CSV path to the config file. """
    utils.add_csv_path_to_config(csv_path)


@app.command()
def due_soon():
    utils.check_csv(CSV_FILE)
    assignemtns_due_soon = utils.get_assignments_due_soon(CSV_FILE, DAYS_NOTICE)
    table = Table('Assignment', 'Class', 'Due Date', 'Days Left', 'Status', header_style='bold blue', row_styles=['yellow'])
    for assignment in assignemtns_due_soon.values():
        table.add_row(assignment[0], assignment[1], str(assignment[2]), str(assignment[3]), assignment[4])
    console.print(table)


@app.command()
def update_status():
    due_soon()

    class_name = Prompt.ask('[bold blue]Which class is the assignment for?[/bold blue]', choices=CLASS_LIST)
    assignment_name = Prompt.ask('[bold blue]Which assignment would you like to update?[/bold blue]', choices=ASSIGNMENT_LIST[class_name])
    status = Prompt.ask('[bold blue]What is the new status?[/bold blue]', choices=STATUS_LIST)

    utils.update_status_value(CSV_FILE, class_name, assignment_name, status)

    print('\n[bold green]Status updated![/bold green]')
    due_soon()


@app.command()
def add_assignment():
    due_soon()
    class_name = Prompt.ask('[bold blue]Which class is the assignment for?[/bold blue]', choices=CLASS_LIST)
    assignment_name = Prompt.ask('[bold blue]What is the name of the assignment?[/bold blue]')
    due_date = Prompt.ask('[bold blue]What is the due date?[/bold blue] (mm/dd/yyyy)', default=datetime.date.today().strftime('%m/%d/%Y'))
    if assignment_name in ASSIGNMENT_LIST[class_name]:
        print('[bold red]Assignment already exists![/bold red]')
        return

    utils.add_assignment_to_csv(CSV_FILE, class_name, assignment_name, due_date)
    print('[bold green]Assignment added![/bold green]')


@app.command()
def remove_assignment():
    due_soon()
    class_name = Prompt.ask('[bold blue]Which class is the assignment for?[/bold blue]', choices=CLASS_LIST)
    assignment_name = Prompt.ask('[bold blue]Which assignment would you like to remove?[/bold blue]', choices=ASSIGNMENT_LIST[class_name])

    utils.remove_assignment_from_csv(CSV_FILE, class_name, assignment_name)
    print('[bold red]Assignment removed![/bold red]')


if __name__ == '__main__':
    app()
