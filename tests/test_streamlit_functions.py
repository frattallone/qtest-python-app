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
    @patch('streamlit.markdown')
    def test_dark_mode_toggle(self, mock_markdown, mock_rerun):
        """Test that the dark mode toggle works correctly."""
        # Import the main function and apply_dark_mode function from app.py
        from src.app import main, apply_dark_mode
        
        # Mock session_state to simulate dark mode toggle
        with patch('streamlit.session_state') as mock_session_state:
            # Set up the mock for session state
            mock_session_state.__contains__.side_effect = lambda key: key in ['language', 'dark_mode']
            mock_session_state.language = 'en'
            mock_session_state.dark_mode = False
            mock_session_state.get.return_value = False
            
            # Mock sidebar toggle to return True (dark mode enabled)
            with patch('streamlit.sidebar.toggle', return_value=True):
                # Mock other necessary Streamlit functions to prevent errors
                with patch('streamlit.set_page_config'), \
                     patch('streamlit.title'), \
                     patch('streamlit.write'), \
                     patch('streamlit.sidebar.title'), \
                     patch('streamlit.sidebar.selectbox', return_value='en'), \
                     patch('streamlit.sidebar.radio', return_value='View Tasks'):
                    
                    # Run the main function
                    main()
                    
                    # Check if st.rerun() was called when dark mode is toggled
                    mock_rerun.assert_called_once()
            
            # Test apply_dark_mode function with dark mode enabled
            mock_session_state.get.return_value = True
            apply_dark_mode()
            
            # Check if st.markdown was called with CSS content
            mock_markdown.assert_called_once()
            css_arg = mock_markdown.call_args[0][0]
            self.assertIn('<style>', css_arg)
            self.assertIn('background-color: #121212', css_arg)


if __name__ == "__main__":
    unittest.main()