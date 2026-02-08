"""Shared pytest fixtures and configuration.

This file is automatically discovered by pytest.
Fixtures defined here are available to all test files.
"""

from __future__ import annotations

import pytest


# ============================================================================
# Example Fixtures (uncomment and modify as needed)
# ============================================================================

# @pytest.fixture
# def sample_data():
#     """Provide sample data for testing.
#
#     Returns:
#         A dictionary with sample data.
#     """
#     return {"key": "value", "number": 42}


# @pytest.fixture
# def temp_file(tmp_path):
#     """Create a temporary test file.
#
#     Args:
#         tmp_path: Built-in pytest fixture providing temporary directory.
#
#     Returns:
#         Path to a temporary test file.
#     """
#     file_path = tmp_path / "test.txt"
#     file_path.write_text("test content")
#     return file_path


# ============================================================================
# Pytest Configuration
# ============================================================================


def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line("markers", "slow: mark test as slow")
    config.addinivalue_line("markers", "integration: mark test as integration test")
