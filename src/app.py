"""
Streamlit web application for the task manager.
"""

import os
import sys
import streamlit as st

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.task_service import TaskService
from src.utils.exceptions import TaskNotFoundException
from src.localization.translations import get_text, LANGUAGES


def main():
    """Main function for the Streamlit application."""
    # Initialize session state for language if it doesn't exist
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    # Get current language
    lang = st.session_state.language
    
    st.set_page_config(
        page_title=get_text("app_title", lang),
        page_icon="✅",
        layout="wide"
    )
    
    st.title(get_text("app_title", lang))
    st.write(get_text("app_subtitle", lang))
    
    # Initialize the task service
    config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
    os.makedirs(config_dir, exist_ok=True)
    storage_file = os.path.join(config_dir, "tasks.json")
    task_service = TaskService(storage_file)
    
    # Sidebar for navigation and language selection
    st.sidebar.title(get_text("navigation", lang))
    
    # Language selector
    selected_language = st.sidebar.selectbox(
        get_text("language", lang),
        options=list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x],
        index=list(LANGUAGES.keys()).index(lang)
    )
    
    # Update language if changed
    if selected_language != lang:
        st.session_state.language = selected_language
        st.rerun()
    
    # Navigation options
    page = st.sidebar.radio(
        "Go to", 
        [
            get_text("view_tasks", lang), 
            get_text("add_task", lang), 
            get_text("search_tasks", lang)
        ]
    )
    
    if page == get_text("view_tasks", lang):
        display_tasks_page(task_service, lang)
    elif page == get_text("add_task", lang):
        add_task_page(task_service, lang)
    elif page == get_text("search_tasks", lang):
        search_tasks_page(task_service, lang)


def display_tasks_page(task_service, lang):
    """Display the tasks page."""
    st.header(get_text("your_tasks", lang))
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        show_completed = st.checkbox(get_text("show_completed_tasks", lang), value=False)
    with col2:
        filter_priority = st.selectbox(
            get_text("filter_by_priority", lang),
            [
                get_text("all", lang), 
                get_text("low", lang), 
                get_text("medium", lang), 
                get_text("high", lang)
            ]
        )
    
    # Get tasks
    tasks = task_service.get_all_tasks(show_completed=True)
    
    # Apply filters
    if not show_completed:
        tasks = [task for task in tasks if not task.completed]
    
    if filter_priority != get_text("all", lang):
        # Map localized priority back to English for filtering
        priority_map = {
            get_text("low", lang): "low",
            get_text("medium", lang): "medium",
            get_text("high", lang): "high"
        }
        filter_priority_en = priority_map.get(filter_priority, "all")
        if filter_priority_en != "all":
            tasks = [task for task in tasks if task.priority.lower() == filter_priority_en]
    
    if not tasks:
        st.info(get_text("no_tasks_found", lang))
        return
    
    # Display tasks
    for task in tasks:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                if task.completed:
                    st.markdown(f"~~**{task.title}**~~")
                else:
                    st.markdown(f"**{task.title}**")
                
                with st.expander(get_text("details", lang)):
                    st.write(f"**{get_text('description', lang)}:** {task.description}")
                    st.write(f"**{get_text('created_at', lang)}:** {task.created_at}")
            
            with col2:
                # Map English priority to localized display
                priority_display = {
                    "low": get_text("low", lang),
                    "medium": get_text("medium", lang),
                    "high": get_text("high", lang)
                }.get(task.priority.lower(), task.priority)
                
                priority_color = {
                    "low": "blue",
                    "medium": "orange",
                    "high": "red"
                }.get(task.priority.lower(), "gray")
                
                st.markdown(
                    f"<span style='color:{priority_color};font-weight:bold;'>{priority_display.upper()}</span>",
                    unsafe_allow_html=True
                )
            
            with col3:
                if not task.completed and st.button("✓", key=f"complete_{task.id}"):
                    task_service.complete_task(task.id)
                    st.rerun()
            
            st.divider()


def add_task_page(task_service, lang):
    """Display the add task page."""
    st.header(get_text("add_new_task", lang))
    
    with st.form("add_task_form"):
        title = st.text_input(get_text("title", lang), max_chars=50)
        description = st.text_area(get_text("description", lang), max_chars=200)
        priority = st.select_slider(
            get_text("priority", lang),
            options=[get_text("low", lang), get_text("medium", lang), get_text("high", lang)],
            value=get_text("medium", lang)
        )
        
        submitted = st.form_submit_button(get_text("add_task", lang))
        
        if submitted:
            if not title:
                st.error(get_text("title_required", lang))
            else:
                # Map localized priority back to English for storage
                priority_map = {
                    get_text("low", lang): "low",
                    get_text("medium", lang): "medium",
                    get_text("high", lang): "high"
                }
                priority_en = priority_map.get(priority, "medium")
                
                task = task_service.add_task(
                    title=title,
                    description=description,
                    priority=priority_en
                )
                st.success(get_text("task_added_success", lang).format(title=title, id=task.id))


def search_tasks_page(task_service, lang):
    """Display the search tasks page."""
    st.header(get_text("search_tasks", lang))
    
    keyword = st.text_input(get_text("search_for_tasks", lang), placeholder=get_text("enter_keyword", lang))
    
    if keyword:
        results = task_service.search_tasks(keyword)
        
        if not results:
            st.info(get_text("no_tasks_matching", lang).format(keyword=keyword))
        else:
            st.write(get_text("found_tasks_matching", lang).format(count=len(results), keyword=keyword))
            
            for task in results:
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        status = get_text("completed", lang) if task.completed else get_text("active", lang)
                        st.markdown(f"**{task.title}** ({status})")
                        
                        # Map English priority to localized display
                        priority_display = {
                            "low": get_text("low", lang),
                            "medium": get_text("medium", lang),
                            "high": get_text("high", lang)
                        }.get(task.priority.lower(), task.priority)
                        
                        st.write(f"{get_text('priority', lang)}: {priority_display}")
                        
                        with st.expander(get_text("details", lang)):
                            st.write(f"**{get_text('description', lang)}:** {task.description}")
                            st.write(f"**{get_text('created_at', lang)}:** {task.created_at}")
                    
                    with col2:
                        if st.button(get_text("view", lang), key=f"view_{task.id}"):
                            st.session_state.task_to_view = task.id
                            st.rerun()
                    
                    st.divider()
    
    # View task details if selected
    if hasattr(st.session_state, 'task_to_view'):
        try:
            task = task_service.get_task_by_id(st.session_state.task_to_view)
            
            st.subheader(get_text("task_details", lang).format(title=task.title))
            st.write(f"**{get_text('id', lang)}:** {task.id}")
            st.write(f"**{get_text('description', lang)}:** {task.description}")
            
            # Map English priority to localized display
            priority_display = {
                "low": get_text("low", lang),
                "medium": get_text("medium", lang),
                "high": get_text("high", lang)
            }.get(task.priority.lower(), task.priority)
            
            st.write(f"**{get_text('priority', lang)}:** {priority_display}")
            
            status = get_text("completed", lang) if task.completed else get_text("active", lang)
            st.write(f"**{get_text('status', lang)}:** {status}")
            st.write(f"**{get_text('created_at', lang)}:** {task.created_at}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if not task.completed and st.button(get_text("mark_as_complete", lang)):
                    task_service.complete_task(task.id)
                    st.rerun()
            
            with col2:
                if st.button(get_text("close", lang)):
                    del st.session_state.task_to_view
                    st.rerun()
                
        except TaskNotFoundException:
            st.error(get_text("task_not_found", lang))
            del st.session_state.task_to_view


if __name__ == "__main__":
    main()
