"""
Tests for the CLI functionality.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cli import main
from src.models.task import Task


class TestCLI(unittest.TestCase):
    """Test cases for the CLI functionality."""

    @patch('sys.argv', ['cli.py', '-h'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_help_command(self, mock_stdout):
        """Test that the help command works correctly."""
        with self.assertRaises(SystemExit):
            main()
        output = mock_stdout.getvalue()
        self.assertIn("Task Manager - A CLI task management app", output)
        self.assertIn("add", output)
        self.assertIn("list", output)
        self.assertIn("complete", output)
        self.assertIn("delete", output)
        self.assertIn("search", output)
        self.assertIn("view", output)

    @patch('sys.argv', ['cli.py', 'add', 'Test Task'])
    @patch('src.cli.TaskService')
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_command(self, mock_stdout, mock_task_service):
        """Test that the add command works correctly."""
        # Setup mock
        mock_task = MagicMock(spec=Task)
        mock_task.id = 1
        mock_task.title = "Test Task"
        mock_task_service_instance = mock_task_service.return_value
        mock_task_service_instance.add_task.return_value = mock_task

        # Run command
        main()

        # Verify
        mock_task_service_instance.add_task.assert_called_once_with("Test Task", "", "medium")
        output = mock_stdout.getvalue()
        self.assertIn("Test Task", output)
        self.assertIn("1", output)

    @patch('sys.argv', ['cli.py', 'list'])
    @patch('src.cli.TaskService')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_command(self, mock_stdout, mock_task_service):
        """Test that the list command works correctly."""
        # Setup mock
        mock_task1 = MagicMock(spec=Task)
        mock_task1.id = 1
        mock_task1.title = "Task 1"
        mock_task1.priority = "high"
        mock_task1.completed = False
        mock_task1.created_at = "2023-01-01 12:00:00"

        mock_task2 = MagicMock(spec=Task)
        mock_task2.id = 2
        mock_task2.title = "Task 2"
        mock_task2.priority = "medium"
        mock_task2.completed = True
        mock_task2.created_at = "2023-01-02 12:00:00"

        mock_task_service_instance = mock_task_service.return_value
        mock_task_service_instance.get_all_tasks.return_value = [mock_task1, mock_task2]

        # Run command
        main()

        # Verify
        mock_task_service_instance.get_all_tasks.assert_called_once_with(show_completed=False)
        output = mock_stdout.getvalue()
        self.assertIn("Task 1", output)
        self.assertIn("Task 2", output)
        self.assertIn("high", output.lower())
        self.assertIn("medium", output.lower())

    @patch('sys.argv', ['cli.py', 'complete', '1'])
    @patch('src.cli.TaskService')
    @patch('sys.stdout', new_callable=StringIO)
    def test_complete_command(self, mock_stdout, mock_task_service):
        """Test that the complete command works correctly."""
        # Setup mock
        mock_task = MagicMock(spec=Task)
        mock_task.id = 1
        mock_task_service_instance = mock_task_service.return_value
        mock_task_service_instance.complete_task.return_value = mock_task

        # Run command
        main()

        # Verify
        mock_task_service_instance.complete_task.assert_called_once_with(1)
        output = mock_stdout.getvalue()
        self.assertIn("1", output)

    @patch('sys.argv', ['cli.py', 'delete', '1'])
    @patch('src.cli.TaskService')
    @patch('sys.stdout', new_callable=StringIO)
    def test_delete_command(self, mock_stdout, mock_task_service):
        """Test that the delete command works correctly."""
        # Setup mock
        mock_task = MagicMock(spec=Task)
        mock_task.id = 1
        mock_task.title = "Test Task"
        mock_task_service_instance = mock_task_service.return_value
        mock_task_service_instance.delete_task.return_value = mock_task

        # Run command
        main()

        # Verify
        mock_task_service_instance.delete_task.assert_called_once_with(1)
        output = mock_stdout.getvalue()
        self.assertIn("Test Task", output)

    @patch('sys.argv', ['cli.py', 'search', 'test'])
    @patch('src.cli.TaskService')
    @patch('sys.stdout', new_callable=StringIO)
    def test_search_command(self, mock_stdout, mock_task_service):
        """Test that the search command works correctly."""
        # Setup mock
        mock_task = MagicMock(spec=Task)
        mock_task.id = 1
        mock_task.title = "Test Task"
        mock_task.priority = "medium"
        mock_task.completed = False
        mock_task_service_instance = mock_task_service.return_value
        mock_task_service_instance.search_tasks.return_value = [mock_task]

        # Run command
        main()

        # Verify
        mock_task_service_instance.search_tasks.assert_called_once_with("test")
        output = mock_stdout.getvalue()
        self.assertIn("Test Task", output)
        self.assertIn("1", output)

    @patch('sys.argv', ['cli.py', 'view', '1'])
    @patch('src.cli.TaskService')
    @patch('sys.stdout', new_callable=StringIO)
    def test_view_command(self, mock_stdout, mock_task_service):
        """Test that the view command works correctly."""
        # Setup mock
        mock_task = MagicMock(spec=Task)
        mock_task.id = 1
        mock_task.title = "Test Task"
        mock_task.description = "Test Description"
        mock_task.priority = "medium"
        mock_task.completed = False
        mock_task.created_at = "2023-01-01 12:00:00"
        mock_task_service_instance = mock_task_service.return_value
        mock_task_service_instance.get_task_by_id.return_value = mock_task

        # Run command
        main()

        # Verify
        mock_task_service_instance.get_task_by_id.assert_called_once_with(1)
        output = mock_stdout.getvalue()
        self.assertIn("Test Task", output)
        self.assertIn("Test Description", output)
        self.assertIn("medium", output.lower())
        self.assertIn("2023-01-01", output)


if __name__ == '__main__':
    unittest.main()