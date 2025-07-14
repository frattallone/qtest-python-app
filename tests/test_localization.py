"""
Tests for the localization module.
"""

import os
import sys
import unittest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.localization.translations import get_text, load_translations, LANGUAGES


class TestLocalization(unittest.TestCase):
    """Test cases for the localization module."""

    def test_available_languages(self):
        """Test that the expected languages are available."""
        self.assertIn("en", LANGUAGES)
        self.assertIn("it", LANGUAGES)
        self.assertEqual(LANGUAGES["en"], "English")
        self.assertEqual(LANGUAGES["it"], "Italiano")

    def test_load_translations(self):
        """Test loading translations for different languages."""
        en_translations = load_translations("en")
        it_translations = load_translations("it")
        
        # Check that translations were loaded
        self.assertIsInstance(en_translations, dict)
        self.assertIsInstance(it_translations, dict)
        
        # Check that translations are not empty
        self.assertGreater(len(en_translations), 0)
        self.assertGreater(len(it_translations), 0)

    def test_get_text(self):
        """Test getting translated text."""
        # Test English translations
        self.assertEqual(get_text("app_title", "en"), "Task Manager")
        self.assertEqual(get_text("add_task", "en"), "Add Task")
        
        # Test Italian translations
        self.assertEqual(get_text("app_title", "it"), "Gestore Attività")
        self.assertEqual(get_text("add_task", "it"), "Aggiungi Attività")
        
        # Test fallback for missing key
        missing_key = "this_key_does_not_exist"
        self.assertEqual(get_text(missing_key, "en"), missing_key)
        self.assertEqual(get_text(missing_key, "it"), missing_key)

    def test_format_strings(self):
        """Test string formatting in translations."""
        # Test English format strings
        task_added_en = get_text("task_added_success", "en").format(title="Test", id=1)
        self.assertIn("Test", task_added_en)
        self.assertIn("1", task_added_en)
        
        # Test Italian format strings
        task_added_it = get_text("task_added_success", "it").format(title="Test", id=1)
        self.assertIn("Test", task_added_it)
        self.assertIn("1", task_added_it)


if __name__ == "__main__":
    unittest.main()