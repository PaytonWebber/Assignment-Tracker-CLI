#!/home/paytonwebber/scripts/assignment_notification/env/bin/python3
import csv
import datetime
import typer
from typing_extensions import Annotated
from rich.prompt import Prompt
from rich import print
from rich.console import Console
from rich.table import Table
from rich.style import Style

ASSIGNMENT_LIST = {"GEOG 104": [], "STAT 260": [], "CSC 360": [], "CSC 305": [], "SENG 321": []}
CLASS_LIST = ["GEOG 104", "STAT 260", "CSC 360", "CSC 305", "SENG 321"]
STATUS_LIST = ["COMPLETED", "IN PROGRESS", "NOT STARTED"]

CSV_FILE = '/home/paytonwebber/scripts/assignment_notification/fall_assignment_list.csv'
DAYS_NOTICE = 14

def complete_class(incomplete: str):
    completion = []
    for course in CLASS_LIST:
        if course.startswith(incomplete):
            completion.append(course)
    return completion

def complete_assignment(incomplete: str):
    completion = []
    # Loop through each element in the ASSIGNMENT_LIST dictionary
    for course in ASSIGNMENT_LIST:
        # Loop through each assignment in the current course
        for assignment in ASSIGNMENT_LIST[course]:
            if assignment.startswith(incomplete):
                completion.append(assignment)
    return completion

def complete_status(incomplete: str):
    completion = []
    for status in STATUS_LIST:
        if status.startswith(incomplete):
            completion.append(status)
    return completion

def callback():
    print('Running a command')

app = typer.Typer()
console = Console()

@app.command()
def main():
    current_date = datetime.datetime.now()

    due_soon = []
    with open(CSV_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader) # skip header row

        for row in reader:
            if row[3] == '' or row[5] == 'COMPLETED': continue

            assignment_name, course, due_date, status = row[0], row[1], datetime.datetime.strptime(row[3], '%m/%d/%Y').date(), row[5]

            if (due_date - current_date.date()).days > DAYS_NOTICE: continue

            days_left = (due_date - current_date.date()).days
            due_soon.append((course, assignment_name, due_date, days_left, status))

    # Sort assignments by due date
    due_soon.sort(key=lambda x: x[2])
    global ASSIGNMENT_LIST

    table = Table('Class', 'Assignment', 'Due Date', 'Days Left', 'Status', header_style='bold blue', row_styles=['yellow'])
    for assignment in due_soon:
        table.add_row(assignment[0], assignment[1], str(assignment[2]), str(assignment[3]), assignment[4])
        if assignment[1] not in ASSIGNMENT_LIST: ASSIGNMENT_LIST[assignment[0]].append(assignment[1])

    console.print(table)

@app.command()
def update_status():
    main()
    class_name = Prompt.ask('[bold blue]Which class is the assignment for?[/bold blue]', choices=CLASS_LIST, autocomplete=complete_class)
    assignment_name = Prompt.ask('[bold blue]Which assignment would you like to update?[/bold blue]', choices=ASSIGNMENT_LIST[class_name], autocomplete=complete_assignment)
    status = Prompt.ask('[bold blue]What is the new status?[/bold blue]', choices=STATUS_LIST, autocomplete=complete_status)

    rows = []
    with open(CSV_FILE, 'r') as f:
        reader = csv.reader(f)
        assignment_found = False
        for row in reader:
            if row[0] == assignment_name and row[1] == class_name:
                row[5] = status
                assignment_found = True
            rows.append(row)
        if not assignment_found:
            print('[bold red]Assignment not found[/bold red]\n')
        else:
            print('[bold green]Assignment updated[/bold green]\n')
    
    with open(CSV_FILE, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

if __name__ == '__main__':
    app()
