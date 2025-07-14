# Task Manager

A simple task management application with both CLI and web interfaces.

## Features

- Add, view, update the tasks
- Mark tasks as complete
- Search for tasks by keyword
- Filter tasks by status and priority
- Command-line interface for quick task management
- Web interface built with Streamlit for a user-friendly experience
- Multi-language support (English and Italian)
- Multiple visual themes including Dark Mode and Psychedelic Mode

## Project Structure

```
task_manager_project/
├── config/                 # Configuration files and task storage
├── docs/                   # Documentation
├── src/                    # Source code
│   ├── localization/       # Localization files
│   │   ├── translations.py # Translation functions
│   │   ├── en.json         # English translations
│   │   └── it.json         # Italian translations
│   ├── models/             # Data models
│   │   └── task.py         # Task model
│   ├── services/           # Business logic
│   │   └── task_service.py # Task management service
│   ├── utils/              # Utility modules
│   │   └── exceptions.py   # Custom exceptions
│   ├── app.py              # Streamlit web application
│   └── cli.py              # Command-line interface
├── tests/                  # Test cases
│   ├── test_task_model.py  # Tests for Task model
│   ├── test_task_service.py# Tests for TaskService
│   ├── test_localization.py# Tests for localization
│   └── test_streamlit_functions.py # Tests for Streamlit functionality
└── requirements.txt        # Project dependencies
```

## Recent Updates

- Updated Streamlit function calls from `st.experimental_rerun()` to `st.rerun()` to be compatible with newer Streamlit versions
- Added test case for Streamlit functionality

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd task_manager_project
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command-line Interface

Run the CLI application:

```
python -m src.cli
```

Available commands:

- Add a task: `python -m src.cli add "Task title" -d "Task description" -p high`
- List tasks: `python -m src.cli list`
- List all tasks including completed: `python -m src.cli list -a`
- Complete a task: `python -m src.cli complete <task-id>`
- Delete a task: `python -m src.cli delete <task-id>`
- Search for tasks: `python -m src.cli search <keyword>`
- View task details: `python -m src.cli view <task-id>`

To change the language:

```
python -m src.cli --language it  # For Italian
python -m src.cli --language en  # For English (default)
```

You can also set the `TASK_MANAGER_LANG` environment variable to set the default language:

```
export TASK_MANAGER_LANG=it  # For Linux/Mac
set TASK_MANAGER_LANG=it     # For Windows
```

### Web Interface

Run the Streamlit web application:

```
streamlit run src/app.py
```

The web interface provides the following pages:
- View Tasks: Display and manage all tasks
- Add Task: Create new tasks
- Search Tasks: Find tasks by keyword

You can change the language using the dropdown in the sidebar.

### Visual Themes

The web interface supports multiple visual themes:
- **Light Mode** (default): Clean, bright interface
- **Dark Mode**: Dark theme for reduced eye strain
- **Psychedelic Mode**: Vibrant, animated theme with rainbow gradients and glowing effects

Toggle between themes using the controls in the sidebar. Note that Psychedelic Mode overrides Dark Mode when enabled.

## Testing

Run the tests:

```
pytest
```

## License

[MIT License](LICENSE)
