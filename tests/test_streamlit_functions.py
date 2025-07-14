"""
Tests for Streamlit functionality in the application.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestStreamlitFunctions(unittest.TestCase):
    """Test cases for Streamlit functionality."""

    @patch('streamlit.rerun')
    def test_streamlit_rerun_function(self, mock_rerun):
        """Test that the application uses st.rerun() instead of st.experimental_rerun()."""
        # Import the main function from app.py
        from src.app import main
        
        # Mock session_state to simulate language change
        with patch('streamlit.session_state') as mock_session_state:
            # Set up the mock to trigger a language change
            mock_session_state.__contains__.return_value = True  # 'language' in st.session_state
            mock_session_state.language = 'en'
            
            # Mock sidebar selectbox to return a different language
            with patch('streamlit.sidebar.selectbox', return_value='it'):
                # Mock other necessary Streamlit functions to prevent errors
                with patch('streamlit.set_page_config'), \
                     patch('streamlit.title'), \
                     patch('streamlit.write'), \
                     patch('streamlit.sidebar.title'), \
                     patch('streamlit.sidebar.radio', return_value='View Tasks'), \
                     patch('streamlit.sidebar.toggle', return_value=False):
                    
                    # Run the main function
                    main()
                    
                    # Check if st.rerun() was called
                    mock_rerun.assert_called_once()

    @patch('streamlit.rerun')
    def test_dark_mode_toggle_main(self, mock_rerun):
        """Test that dark mode toggle in main() triggers rerun."""
        # Import the main function
        from src.app import main
        
        # Mock session_state to simulate dark mode toggle
        with patch('streamlit.session_state') as mock_session_state:
            # Set up the mock for session state
            mock_session_state.__contains__.side_effect = lambda key: key in ['language', 'dark_mode']
            mock_session_state.language = 'en'
            mock_session_state.dark_mode = False
            mock_session_state.get.return_value = False
            
            # Mock TaskService and task list to avoid any task rendering
            mock_task_service = MagicMock()
            mock_task_service.get_tasks.return_value = []
            mock_task_service.get_task.return_value = None
            mock_task_service.get_task_by_title.return_value = None
            mock_task_service.search_tasks.return_value = []

            # Mock sidebar toggle to return True (dark mode enabled)
            # Import our mock columns
            from tests.mock_columns import create_mock_columns
            
            with patch('streamlit.sidebar.toggle', return_value=True), \
                 patch('src.app.TaskService', return_value=mock_task_service), \
                 patch('streamlit.markdown'), \
                 patch('streamlit.set_page_config'), \
                 patch('streamlit.container'), \
                 patch('streamlit.columns', return_value=create_mock_columns(2)), \
                 patch('streamlit.expander'), \
                 patch('streamlit.title'), \
                 patch('streamlit.header'), \
                 patch('streamlit.write'), \
                 patch('streamlit.sidebar.title'), \
                 patch('streamlit.sidebar.selectbox', return_value='en'), \
                 patch('streamlit.sidebar.radio', return_value='View Tasks'), \
                 patch('streamlit.radio', return_value='all'):
                
                # Run the main function
                main()
                
                # Check if st.rerun() was called when dark mode is toggled
                mock_rerun.assert_called_once()

    def test_apply_dark_mode(self):
        """Test that apply_dark_mode applies dark mode CSS when enabled and psychedelic mode is disabled."""
        # Import apply_dark_mode function
        from src.app import apply_dark_mode

        # Create new mocks for streamlit functions
        with patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.session_state') as mock_session_state:

            # Configure session state for dark mode enabled, psychedelic mode disabled
            def mock_get(key, default=False):
                if key == 'dark_mode':
                    return True
                elif key == 'psychedelic_mode':
                    return False
                return default
            
            mock_session_state.get.side_effect = mock_get
            
            # Apply dark mode
            apply_dark_mode()

            # Verify markdown was called once with CSS
            self.assertEqual(mock_markdown.call_count, 1)
            css_arg = mock_markdown.call_args[0][0]
            self.assertIn('<style>', css_arg)
            self.assertIn('background-color: #121212', css_arg)
    
    def test_apply_psychedelic_mode(self):
        """Test that apply_psychedelic_mode applies psychedelic CSS when enabled."""
        # Import apply_psychedelic_mode function
        from src.app import apply_psychedelic_mode

        # Create new mocks for streamlit functions
        with patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.session_state') as mock_session_state:

            # Configure session state for psychedelic mode enabled
            mock_session_state.get.return_value = True
            
            # Apply psychedelic mode
            apply_psychedelic_mode()

            # Verify markdown was called once with CSS
            self.assertEqual(mock_markdown.call_count, 1)
            css_arg = mock_markdown.call_args[0][0]
            self.assertIn('<style>', css_arg)
            self.assertIn('linear-gradient', css_arg)
            self.assertIn('animation: rainbow', css_arg)


if __name__ == "__main__":
    unittest.main()
