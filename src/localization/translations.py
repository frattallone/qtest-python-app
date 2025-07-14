"""
Translation functions for the task manager application.
"""

import json
import os
from typing import Dict, Any

# Available languages
LANGUAGES = {
    "en": "English",
    "it": "Italiano"
}

# Default language
DEFAULT_LANGUAGE = "en"

# Cache for loaded translations
_translations: Dict[str, Dict[str, str]] = {}


def load_translations(lang_code: str) -> Dict[str, str]:
    """
    Load translations for the specified language.
    
    Args:
        lang_code: Language code (e.g., 'en', 'it')
        
    Returns:
        Dictionary of translations
    """
    # Return from cache if already loaded
    if lang_code in _translations:
        return _translations[lang_code]
    
    # Get the path to the translation file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    lang_file = os.path.join(base_dir, f"{lang_code}.json")
    
    # Load translations from file
    try:
        with open(lang_file, "r", encoding="utf-8") as f:
            translations = json.load(f)
        _translations[lang_code] = translations
        return translations
    except (FileNotFoundError, json.JSONDecodeError):
        # If the requested language file doesn't exist or is invalid,
        # fall back to the default language
        if lang_code != DEFAULT_LANGUAGE:
            print(f"Warning: Translation file for '{lang_code}' not found or invalid. "
                  f"Falling back to {DEFAULT_LANGUAGE}.")
            return load_translations(DEFAULT_LANGUAGE)
        else:
            # If even the default language file is missing, return an empty dict
            print(f"Error: Default translation file '{DEFAULT_LANGUAGE}.json' not found or invalid.")
            return {}


def get_text(key: str, lang_code: str = DEFAULT_LANGUAGE) -> str:
    """
    Get the translated text for a given key.
    
    Args:
        key: Translation key
        lang_code: Language code (e.g., 'en', 'it')
        
    Returns:
        Translated text or the key itself if translation is not found
    """
    translations = load_translations(lang_code)
    return translations.get(key, key)