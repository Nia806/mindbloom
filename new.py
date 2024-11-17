import csv
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

TASKS_FILE = 'tasks.csv'

# Initialize tasks file if it doesn't exist
if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Description', 'Due Date', 'Status'])  

def get_tasks():
    with open(TASKS_FILE, 'r') as file:
        reader = csv.reader(file)
        tasks = list(reader)[1:]  # Skip header row
    return tasks

def add_task_to_file(description, due_date):
    with open(TASKS_FILE, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        task_id = len(rows)  # New ID based on the number of tasks

    with open(TASKS_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([task_id, description, due_date, 'Pending'])

@app.route('/')
def index():
    tasks = get_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    description = request.form['description']
    due_date = request.form['due_date']
    
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD.", 400
    
    add_task_to_file(description, due_date)
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    tasks = get_tasks()
    for task in tasks:
        if int(task[0]) == task_id:
            task[3] = 'Completed'
            break
    
    # Write back the updated tasks to the file
    with open(TASKS_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Description', 'Due Date', 'Status'])  # Write header
        writer.writerows(tasks)
    
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks = get_tasks()
    tasks = [task for task in tasks if int(task[0]) != task_id]
    
    # Write back the updated tasks to the file
    with open(TASKS_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Description', 'Due Date', 'Status'])  # Write header
        writer.writerows(tasks)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
