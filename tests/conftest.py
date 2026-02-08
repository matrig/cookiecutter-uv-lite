"""Shared pytest fixtures for cookiecutter-uv-lite tests."""

from __future__ import annotations

import os

import pytest

from tests.utils import run_within_dir


@pytest.fixture
def baked_project(cookies, tmp_path):
    """Fixture that bakes a project with default settings.

    Returns a callable that accepts extra_context kwargs and returns
    the baked project result with assertions that baking succeeded.
    """

    def _bake(**extra_context):
        # Extract special _needs_install flag
        needs_install = extra_context.pop("_needs_install", False)

        # Default to git_repo=n to avoid interactive prompts in tests
        context = {"git_repo": "n", **extra_context}

        # Skip install by default for performance (unless test needs it)
        original_skip = os.environ.get("COOKIECUTTER_SKIP_INSTALL")
        if not needs_install:
            os.environ["COOKIECUTTER_SKIP_INSTALL"] = "true"

        try:
            with run_within_dir(tmp_path):
                result = cookies.bake(extra_context=context)
                assert result.exit_code == 0, f"Baking failed: {result.exception}"
                assert result.project_path.is_dir()
                return result
        finally:
            # Restore original environment
            if not needs_install:
                if original_skip is None:
                    os.environ.pop("COOKIECUTTER_SKIP_INSTALL", None)
                else:
                    os.environ["COOKIECUTTER_SKIP_INSTALL"] = original_skip

    return _bake
