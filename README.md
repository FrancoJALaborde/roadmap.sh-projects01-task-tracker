## Create and Activate a Virtual Environment on Windows

#(Project URL https://roadmap.sh/projects/task-tracker)

1. Open the terminal (cmd) and navigate to your project folder:

   cd path\to\your\project

2. Create the virtual environment:

   python -m venv venv

3. Activate the virtual environment:

   venv\Scripts\activate

4. (Optional) Install the required packages:

   pip install package_name

5. To deactivate the virtual environment:

   deactivate


## Task Tracker CLI - Command Examples

This section provides examples of all available commands for the interactive Task Tracker CLI.  
Type these commands inside the CLI prompt after starting the program.

## Run the file: 

python app/task_cli.py

## Run the tests

python -m tests.test_task_cli

---

### 1. Add a New Task

add Buy milk and bread

_Adds a new task with the description "Buy milk and bread"._

---

### 2. Update a task

update 1 Buy milk, bread and eggs

_Updates the task with ID 1, changing its description to "Buy milk, bread, and eggs"._

---

### 3. Delete a task

delete 1

_Deletes the task with ID 1._

---

### 4. Mark a task as "in progress"

mark-in-progress 2

_Sets the status of the task with ID 2 to "in-progress"._

---

### 5. Mark a task as "done"

mark-done 2

_Sets the status of the task with ID 2 to "done"._

---

### 6. List all tasks

list

_Displays all tasks, regardless of their status._

---

### 7. List only completed tasks

list done

_Displays only tasks with status "done"._

---

### 8. List only pending tasks
 
list todo

_Displays only tasks with status "todo" (pending)._

---

### 9. List only tasks in progress

list in-progress

_Displays only tasks with status "in-progress"._

---

### 10. Show help

help

_Displays all available commands and their usage._

---

### 11. Exit the program

exit

_Closes the interactive Task Tracker CLI._

