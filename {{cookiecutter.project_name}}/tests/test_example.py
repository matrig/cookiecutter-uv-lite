"""Example tests - replace with your actual tests."""

from __future__ import annotations

import pytest


def test_example():
    """Example test showing basic assertion."""
    assert 1 + 1 == 2


@pytest.mark.parametrize("value,expected", [(0, 0), (1, 1), (2, 4)])
def test_parametrized_example(value, expected):
    """Example showing parametrized test."""
    assert value**2 == expected


# TODO: Replace examples above with your actual tests
# from {{cookiecutter.package_name}} import your_module
# def test_your_function():
#     assert your_module.your_function() == expected_result
