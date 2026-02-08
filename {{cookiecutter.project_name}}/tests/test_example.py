{% set package_name = cookiecutter.project_name|lower|replace('-', '_') -%}
"""Example tests - replace with your actual tests."""

from __future__ import annotations

{% if cookiecutter.project_type == 'cli' %}
from typer.testing import CliRunner

from {{package_name}}.cli import app

runner = CliRunner()


def test_cli_help():
    """Test CLI help command works."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "{{cookiecutter.project_name}}" in result.stdout


def test_cli_hello_default():
    """Test hello command with default name."""
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Hello" in result.stdout


def test_cli_hello_custom():
    """Test hello command with custom name."""
    result = runner.invoke(app, ["hello", "--name", "Alice"])
    assert result.exit_code == 0
    assert "Alice" in result.stdout


def test_cli_version():
    """Test version command."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "version" in result.stdout.lower()


# TODO: Replace examples above with your actual CLI tests

{% else %}
import pytest


def test_example():
    """Example test showing basic assertion."""
    assert 1 + 1 == 2


@pytest.mark.parametrize("value,expected", [(0, 0), (1, 1), (2, 4)])
def test_parametrized_example(value, expected):
    """Example showing parametrized test."""
    assert value**2 == expected


# TODO: Replace examples above with your actual tests
# from {{package_name}} import your_module
# def test_your_function():
#     assert your_module.your_function() == expected_result

{% endif %}
