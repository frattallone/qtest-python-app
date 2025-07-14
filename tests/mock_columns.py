"""Mock columns for testing."""
from unittest.mock import MagicMock

class MockColumn(MagicMock):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

def create_mock_columns(n=2):
    """Create a list of n mock columns."""
    return tuple(MockColumn() for _ in range(n))