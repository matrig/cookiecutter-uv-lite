# Unittesting with Pytest

[pytest](https://docs.pytest.org/en/7.1.x/) is automatically added to the environment, along with [pytest-xdist](https://pytest-xdist.readthedocs.io/) for parallel test execution.

## Test Structure

Generated projects include example tests demonstrating pytest best practices:

- **`tests/test_example.py`** - Example tests showing:

  - Basic assertions
  - Parametrized tests with `@pytest.mark.parametrize`
  - Self-contained examples (don't depend on code that will be deleted)

- **`tests/conftest.py`** - Shared test configuration:
  - Example fixtures (commented out, ready to uncomment)
  - Custom pytest markers (`@pytest.mark.slow`, `@pytest.mark.integration`)
  - Automatically discovered by pytest

## Running Tests

```bash
make test
```

Tests automatically run in parallel using `pytest-xdist` (via `-n auto` flag), which distributes tests across available CPU cores for faster execution. This is especially beneficial as your test suite grows.

## Example Test Pattern

```python
@pytest.mark.parametrize("value,expected", [(0, 0), (1, 1), (2, 4)])
def test_parametrized_example(value, expected):
    """Example showing parametrized test."""
    assert value**2 == expected
```
