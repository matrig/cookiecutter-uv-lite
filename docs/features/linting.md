# Linting and code quality

Code can be linted and quality-checked with the command

```bash
make check
```

This command will run the following tools:

## pre-commit

Generated projects include a `.pre-commit-config.yaml` file that configures git hooks to run checks before each commit. The hooks are automatically installed when you run `make install` (if inside a git repository).

The pre-commit configuration includes:

- File hygiene checks (case conflicts, merge conflicts, trailing whitespace, end-of-file fixer)
- ruff linting and formatting
- prettier for non-Python files

You can also run pre-commit manually:

```bash
# Run on all files
make check

# Run on staged files only
uv run pre-commit run
```

## ruff

[ruff](https://github.com/charliermarsh/ruff) is used to lint and format the code, and it is configured through `pyproject.toml`:

```
[tool.ruff]
target-version = "py311"
line-length = 120
fix = true
select = [
    # flake8-2020
    "YTT",
    # flake8-bandit
    "S",
    # flake8-bugbear
    "B",
    # flake8-builtins
    "A",
    # flake8-comprehensions
    "C4",
    # flake8-debugger
    "T10",
    # flake8-simplify
    "SIM",
    # isort
    "I",
    # mccabe
    "C90",
    # pycodestyle
    "E", "W",
    # pyflakes
    "F",
    # pygrep-hooks
    "PGH",
    # pyupgrade
    "UP",
    # ruff
    "RUF",
    # tryceratops
    "TRY",
]
ignore = [
    # LineTooLong
    "E501",
    # DoNotAssignLambda
    "E731",
]

[tool.ruff.format]
preview = true

[tool.ruff.per-file-ignores]
"tests/*" = ["S101"]
```

# mypy

[mypy](https://mypy.readthedocs.io/en/stable/) is used for static type checking, and it's configuration and can be edited in `pyproject.toml`.

```toml
[tool.mypy]
disallow_untyped_defs = true
disallow_any_unimported = true
no_implicit_optional = true
check_untyped_defs = true
warn_return_any = true
warn_unused_ignores = true
show_error_codes = true
exclude = [
    '\.venv',
    '{{cookiecutter.project_name}}',
    'tests'
]
```

# deptry

[deptry](https://github.com/fpgmaas/deptry) is used to check the code for dependency issues, and it can be configured by adding a `[tool.deptry]` section in `pyproject.toml`. For more information, see [this section](https://deptry.com/usage/#configuration) documentation of deptry.

# Prettier

[Prettier](https://prettier.io/) is used to format the markdown documentation, along with any json and yaml files.
Its options can be configured in the included `.editorconfig` file or in greater detail by adding a `.prettierrc` file ([See Docs](https://prettier.io/docs/en/configuration)).

```yaml
[*]
max_line_length = 120

[*.json]
indent_style = space
indent_size = 4
```

## Github Actions

If `include_github_actions` is set to `"y"`, code formatting is checked
for every merge request, every merge to main, and every release.
