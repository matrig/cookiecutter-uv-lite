"""Shared pytest fixtures for cookiecutter-uv-lite tests."""

from __future__ import annotations

import pytest

from tests.utils import run_within_dir


@pytest.fixture
def baked_project(cookies, tmp_path):
    """Fixture that bakes a project with default settings.

    Returns a callable that accepts extra_context kwargs and returns
    the baked project result with assertions that baking succeeded.
    """

    def _bake(**extra_context):
        # Default to git_repo=n to avoid interactive prompts in tests
        context = {"git_repo": "n", **extra_context}
        with run_within_dir(tmp_path):
            result = cookies.bake(extra_context=context)
            assert result.exit_code == 0, f"Baking failed: {result.exception}"
            assert result.project_path.is_dir()
            return result

    return _bake
