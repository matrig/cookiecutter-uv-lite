"""Test notebook execution and utilities.

{% if cookiecutter.project_type == 'notebooks' -%}
This file contains tests specific to the notebooks project type.
Notebooks are tested via pytest-nbval - run with: pytest --nbval notebooks/
{%- endif %}
"""

from __future__ import annotations

{% if cookiecutter.project_type == 'notebooks' -%}
import pathlib


def test_notebooks_directory_exists():
    """Verify notebooks directory structure."""
    notebooks_dir = pathlib.Path("notebooks")
    assert notebooks_dir.exists()
    assert notebooks_dir.is_dir()
    assert (notebooks_dir / "01-exploratory.ipynb").exists()
    assert (notebooks_dir / "02-visualization.ipynb").exists()


def test_data_directory_exists():
    """Verify data directory structure."""
    data_dir = pathlib.Path("data")
    assert data_dir.exists()
    assert data_dir.is_dir()
{%- endif %}
