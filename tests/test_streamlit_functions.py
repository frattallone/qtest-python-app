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
                     patch('streamlit.sidebar.radio', return_value='View Tasks'):
                    
                    # Run the main function
                    main()
                    
                    # Check if st.rerun() was called
                    mock_rerun.assert_called_once()


if __name__ == "__main__":
    unittest.main()
