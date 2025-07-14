#!/usr/bin/env python3
"""
Command-line interface for the task manager application.
"""

import argparse
import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException
from src.localization.translations import get_text, LANGUAGES


def main():
    """Main function to handle command-line arguments."""
    # Get the language from environment variable if set, otherwise use default
    default_lang = os.environ.get("TASK_MANAGER_LANG", "en")
    
    # Create the main parser
    parser = argparse.ArgumentParser(description="Task Manager - A CLI task management app")
    
    # Add language option to the main parser
    parser.add_argument(
        "-l", "--language", 
        help="Language for the interface", 
        choices=list(LANGUAGES.keys()), 
        default=default_lang
    )
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute", required=True)

    # Add task command
    add_parser = subparsers.add_parser("add", help=get_text("add_task", default_lang))
    add_parser.add_argument("title", help=get_text("title", default_lang))
    add_parser.add_argument("-d", "--description", help=get_text("description", default_lang), default="")
    add_parser.add_argument(
        "-p", "--priority", 
        help=get_text("priority", default_lang), 
        choices=["low", "medium", "high"], 
        default="medium"
    )

    # List tasks command
    list_parser = subparsers.add_parser("list", help=get_text("view_tasks", default_lang))
    list_parser.add_argument(
        "-a", "--all", 
        help=get_text("show_completed_tasks", default_lang), 
        action="store_true"
    )

    # Complete task command
    complete_parser = subparsers.add_parser("complete", help=get_text("mark_as_complete", default_lang))
    complete_parser.add_argument("id", type=int, help=get_text("id", default_lang))

    # Delete task command
    delete_parser = subparsers.add_parser("delete", help=get_text("task_deleted", default_lang))
    delete_parser.add_argument("id", type=int, help=get_text("id", default_lang))

    # Search tasks command
    search_parser = subparsers.add_parser("search", help=get_text("search_tasks", default_lang))
    search_parser.add_argument("keyword", help=get_text("search_for_tasks", default_lang))

    # View task command
    view_parser = subparsers.add_parser("view", help=get_text("view", default_lang))
    view_parser.add_argument("id", type=int, help=get_text("id", default_lang))

    # Parse arguments once after all parsers are defined
    args = parser.parse_args()
    
    # Update language if specified in arguments
    lang = args.language
    
    # Initialize the task service
    config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
    os.makedirs(config_dir, exist_ok=True)
    storage_file = os.path.join(config_dir, "tasks.json")
    task_service = TaskService(storage_file)

    # Language is already set from the parsed arguments

    try:
        if args.command == "add":
            task = task_service.add_task(args.title, args.description, args.priority)
            print(get_text("task_added_success", lang).format(title=task.title, id=task.id))
            
        elif args.command == "list":
            tasks = task_service.get_all_tasks(show_completed=args.all)
            if not tasks:
                print(get_text("no_tasks_found", lang))
                return
                
            print("\n" + "=" * 60)
            print(f"{get_text('id', lang):^5}|{get_text('title', lang):^20}|{get_text('priority', lang):^10}|{get_text('status', lang):^10}|{get_text('created_at', lang):^20}")
            print("=" * 60)
            
            for task in tasks:
                status = get_text("completed", lang) if task.completed else get_text("active", lang)
                
                # Map English priority to localized display
                priority_display = {
                    "low": get_text("low", lang),
                    "medium": get_text("medium", lang),
                    "high": get_text("high", lang)
                }.get(task.priority.lower(), task.priority)
                
                print(f"{task.id:^5}|{task.title[:18]:^20}|{priority_display:^10}|{status:^10}|{task.created_at:^20}")
            
            print("=" * 60 + "\n")
            
        elif args.command == "complete":
            task = task_service.complete_task(args.id)
            print(get_text("task_marked_complete", lang).format(id=task.id))
            
        elif args.command == "delete":
            task = task_service.delete_task(args.id)
            print(get_text("task_deleted", lang).format(title=task.title))
            
        elif args.command == "search":
            results = task_service.search_tasks(args.keyword)
            
            if not results:
                print(get_text("no_tasks_matching", lang).format(keyword=args.keyword))
                return
                
            print(get_text("found_tasks_matching", lang).format(count=len(results), keyword=args.keyword))
            print("=" * 60)
            print(f"{get_text('id', lang):^5}|{get_text('title', lang):^20}|{get_text('priority', lang):^10}|{get_text('status', lang):^10}")
            print("=" * 60)
            
            for task in results:
                status = get_text("completed", lang) if task.completed else get_text("active", lang)
                
                # Map English priority to localized display
                priority_display = {
                    "low": get_text("low", lang),
                    "medium": get_text("medium", lang),
                    "high": get_text("high", lang)
                }.get(task.priority.lower(), task.priority)
                
                print(f"{task.id:^5}|{task.title[:18]:^20}|{priority_display:^10}|{status:^10}")
            
            print("=" * 60 + "\n")
            
        elif args.command == "view":
            task = task_service.get_task_by_id(args.id)
            print("\n" + "=" * 60)
            print(f"{get_text('id', lang)}: {task.id}")
            print(f"{get_text('title', lang)}: {task.title}")
            print(f"{get_text('description', lang)}: {task.description}")
            
            # Map English priority to localized display
            priority_display = {
                "low": get_text("low", lang),
                "medium": get_text("medium", lang),
                "high": get_text("high", lang)
            }.get(task.priority.lower(), task.priority)
            
            print(f"{get_text('priority', lang)}: {priority_display}")
            
            status = get_text("completed", lang) if task.completed else get_text("active", lang)
            print(f"{get_text('status', lang)}: {status}")
            print(f"{get_text('created_at', lang)}: {task.created_at}")
            print("=" * 60 + "\n")
            
        else:
            parser.print_help()
            
    except TaskNotFoundException as e:
        print(get_text("error", lang).format(message=str(e)))
    except Exception as e:
        print(get_text("unexpected_error", lang).format(message=str(e)))


if __name__ == "__main__":
    main()
