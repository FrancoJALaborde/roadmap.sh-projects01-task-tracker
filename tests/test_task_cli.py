import unittest
import os
import json
from datetime import datetime
from app.task_cli import (
    add_task, update_task, delete_task,
    mark_task_status, list_tasks, load_tasks, save_tasks, TASKS_FILE
)

class TestTaskTracker(unittest.TestCase):
    TEST_FILE = 'test_tasks.json'

    def setUp(self):
        # Redefine the TASKS_FILE to use a test file
        global TASKS_FILE
        TASKS_FILE = self.TEST_FILE
        # Start with a clean file
        save_tasks([])

    def tearDown(self):
        # Remove the test file after each test
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_add_task(self):
        task = add_task("Test task")
        self.assertEqual(task['description'], "Test task")
        self.assertEqual(task['status'], "to-do")
        self.assertIsInstance(task['id'], int)
        self.assertIn('createdAt', task)
        self.assertIn('updatedAt', task)
        tasks = load_tasks()
        self.assertEqual(len(tasks), 1)

    def test_update_task(self):
        task = add_task("Original")
        updated = update_task(task['id'], "Updated description")
        self.assertTrue(updated)
        tasks = load_tasks()
        self.assertEqual(tasks[0]['description'], "Updated description")

    def test_delete_task(self):
        task = add_task("To be deleted")
        deleted = delete_task(task['id'])
        self.assertTrue(deleted)
        tasks = load_tasks()
        self.assertEqual(len(tasks), 0)

    def test_mark_in_progress(self):
        task = add_task("Progress task")
        marked = mark_task_status(task['id'], "in-progress")
        self.assertTrue(marked)
        tasks = load_tasks()
        self.assertEqual(tasks[0]['status'], "in-progress")

    def test_mark_done(self):
        task = add_task("Done task")
        marked = mark_task_status(task['id'], "done")
        self.assertTrue(marked)
        tasks = load_tasks()
        self.assertEqual(tasks[0]['status'], "done")

    def test_list_tasks(self):
        add_task("Task 1")
        add_task("Task 2")
        tasks = list_tasks()
        self.assertEqual(len(tasks), 2)

    def test_list_done(self):
        t1 = add_task("Task 1")
        t2 = add_task("Task 2")
        mark_task_status(t2['id'], "done")
        done_tasks = list_tasks("done")
        self.assertEqual(len(done_tasks), 1)
        self.assertEqual(done_tasks[0]['status'], "done")

    def test_list_todo(self):
        t1 = add_task("Task 1")
        t2 = add_task("Task 2")
        mark_task_status(t2['id'], "done")
        todo_tasks = list_tasks("to-do")
        self.assertEqual(len(todo_tasks), 1)
        self.assertEqual(todo_tasks[0]['status'], "to-do")

    def test_list_in_progress(self):
        t1 = add_task("Task 1")
        t2 = add_task("Task 2")
        mark_task_status(t2['id'], "in-progress")
        in_progress_tasks = list_tasks("in-progress")
        self.assertEqual(len(in_progress_tasks), 1)
        self.assertEqual(in_progress_tasks[0]['status'], "in-progress")

    def test_update_nonexistent(self):
        updated = update_task(999, "Should not work")
        self.assertFalse(updated)

    def test_delete_nonexistent(self):
        deleted = delete_task(999)
        self.assertFalse(deleted)

    def test_mark_nonexistent(self):
        marked = mark_task_status(999, "done")
        self.assertFalse(marked)

    def test_invalid_status(self):
        task = add_task("Invalid status test")
        marked = mark_task_status(task['id'], "not-a-status")
        self.assertFalse(marked)

if __name__ == '__main__':
    unittest.main()