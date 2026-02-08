from __future__ import annotations

import shlex
import subprocess
from unittest.mock import patch

import pytest

from tests.utils import file_contains_text, run_within_dir

# Template placeholder for package_name derivation
PACKAGE_NAME_PLACEHOLDER = "{{cookiecutter.project_name|lower|replace('-', '_')}}"

# ============================================================================
# Basic Project Generation Tests
# ============================================================================


@pytest.mark.parametrize("project_type", ["package", "cli"])
def test_bake_project(baked_project, project_type):
    """Test basic project baking with custom name for both project types."""
    result = baked_project(project_name="my-project", project_type=project_type)
    assert result.exception is None
    assert result.project_path.name == "my-project"


def test_using_pytest(baked_project):
    """Test that generated project can run its own tests."""
    result = baked_project(_needs_install=True)

    # Run the tests (environment already installed by hook)
    with run_within_dir(str(result.project_path)):
        assert subprocess.check_call(shlex.split("uv run make test")) == 0


def test_cli_main():
    """Test the CLI main function."""
    from cookiecutter_uv_lite.cli import main

    with patch("os.system") as mock_system:
        main()
        mock_system.assert_called_once()
        assert "cookiecutter" in mock_system.call_args[0][0]


# ============================================================================
# Optional Features Tests
# ============================================================================


@pytest.mark.parametrize(
    "feature,enabled,files_to_check,should_exist",
    [
        # MkDocs feature
        ("mkdocs", "y", ["docs", "mkdocs.yml"], True),
        ("mkdocs", "n", ["docs", "mkdocs.yml"], False),
        # GitHub Actions feature
        ("github_actions", "y", [".github/workflows/ci.yml", ".github/workflows/docs.yml"], True),
        ("github_actions", "n", [".github"], False),
        # Tox config (always present)
        (None, None, ["tox.ini"], True),
    ],
)
def test_optional_files(baked_project, feature, enabled, files_to_check, should_exist):
    """Test that optional features create/remove expected files."""
    context = {feature: enabled} if feature else {}
    result = baked_project(**context)

    for file_path in files_to_check:
        full_path = result.project_path / file_path
        if should_exist:
            assert full_path.exists(), f"Expected {file_path} to exist"
        else:
            assert not full_path.exists(), f"Expected {file_path} to not exist"


@pytest.mark.parametrize(
    "mkdocs,expected_in_makefile",
    [
        ("y", "docs:"),
        ("n", None),
    ],
)
def test_mkdocs_makefile_targets(baked_project, mkdocs, expected_in_makefile):
    """Test that MkDocs-related Makefile targets are conditionally included."""
    result = baked_project(mkdocs=mkdocs)
    makefile = result.project_path / "Makefile"

    if expected_in_makefile:
        assert file_contains_text(str(makefile), expected_in_makefile)
    else:
        assert not file_contains_text(str(makefile), "docs:")


@pytest.mark.parametrize(
    "codecov,github_actions,should_have_codecov",
    [
        ("y", "y", True),  # Codecov enabled with GitHub Actions
        ("n", "y", False),  # Codecov disabled
        ("y", "n", False),  # No CI files at all
    ],
)
def test_codecov_integration(baked_project, codecov, github_actions, should_have_codecov):
    """Test that Codecov integration is conditionally added to CI."""
    result = baked_project(codecov=codecov, github_actions=github_actions)
    ci_file = result.project_path / ".github/workflows/ci.yml"

    if github_actions == "y":
        assert ci_file.exists()
        has_codecov = file_contains_text(str(ci_file), "CODECOV_TOKEN")
        assert has_codecov == should_have_codecov
    else:
        assert not ci_file.exists()


# ============================================================================
# Configuration File Tests
# ============================================================================


@pytest.mark.parametrize("project_type", ["package", "cli"])
@pytest.mark.parametrize(
    "file_path,expected_contents",
    [
        (".pre-commit-config.yaml", ["ruff", "prettier", "pre-commit-hooks"]),
        ("pyproject.toml", ["ruff", "mypy", "pytest"]),
        ("tox.ini", ["[tox]"]),
    ],
)
def test_config_file_content(baked_project, project_type, file_path, expected_contents):
    """Test that configuration files contain expected content for both project types."""
    result = baked_project(project_type=project_type)
    config_file = result.project_path / file_path

    assert config_file.exists(), f"{file_path} should exist"
    for content in expected_contents:
        assert file_contains_text(str(config_file), content), f"{file_path} should contain '{content}'"


@pytest.mark.parametrize(
    "target,expected_content",
    [
        ("check", ["pre-commit run -a", "mypy"]),
        ("install", ["pre-commit install", "if [ -d .git ]"]),
        ("test", ["pytest"]),
        ("build", ["pyproject-build"]),
    ],
)
def test_makefile_targets(baked_project, target, expected_content):
    """Test that Makefile targets contain expected commands."""
    result = baked_project()
    makefile = result.project_path / "Makefile"

    assert makefile.exists()
    for content in expected_content:
        assert file_contains_text(str(makefile), content), f"Makefile should contain '{content}' in {target} target"


# ============================================================================
# Project Naming Tests
# ============================================================================


@pytest.mark.parametrize("project_type", ["package", "cli"])
@pytest.mark.parametrize(
    "project_name,expected_package_name",
    [
        ("my-project", "my_project"),
        ("my-cool-app", "my_cool_app"),
        ("test-123", "test_123"),
        ("a-b-c-d", "a_b_c_d"),
    ],
)
def test_package_name_derivation(baked_project, project_type, project_name, expected_package_name):
    """Test that package names are correctly derived from project names for both types."""
    result = baked_project(project_name=project_name, project_type=project_type)

    assert result.project_path.name == project_name
    package_dir = result.project_path / expected_package_name
    assert package_dir.is_dir(), f"Package directory {expected_package_name} should exist"
    assert (package_dir / "__init__.py").is_file()


@pytest.mark.parametrize(
    "invalid_name,reason",
    [
        ("_invalid", "starts with underscore"),
        ("invalid_name", "contains underscore"),
        ("123invalid", "starts with number"),
    ],
    ids=lambda x: x if isinstance(x, str) and x.startswith("_") or x[0].isdigit() else x.replace("_", "-"),
)
def test_invalid_project_names(cookies, tmp_path, invalid_name, reason):
    """Test that invalid project names are rejected with clear errors."""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"project_name": invalid_name, "git_repo": "n"})
        assert result.exit_code != 0, f"Should reject project name that {reason}"
        assert result.exception is not None


# ============================================================================
# Dependency and Content Tests
# ============================================================================


@pytest.mark.parametrize(
    "mkdocs,should_have_mkdocs_deps",
    [
        ("y", True),
        ("n", False),
    ],
)
def test_mkdocs_dependencies(baked_project, mkdocs, should_have_mkdocs_deps):
    """Test that MkDocs dependencies are conditionally included in pyproject.toml."""
    result = baked_project(mkdocs=mkdocs)
    pyproject = result.project_path / "pyproject.toml"

    assert pyproject.exists()
    has_mkdocs = file_contains_text(str(pyproject), "mkdocs")
    assert has_mkdocs == should_have_mkdocs_deps


@pytest.mark.parametrize("project_type", ["package", "cli"])
def test_pyproject_metadata(baked_project, project_type):
    """Test that pyproject.toml contains correct project metadata for both types."""
    result = baked_project(
        project_name="test-app",
        project_description="A test application",
        project_type=project_type,
    )
    pyproject = result.project_path / "pyproject.toml"

    assert file_contains_text(str(pyproject), 'name = "test-app"')
    assert file_contains_text(str(pyproject), "A test application")


@pytest.mark.parametrize(
    "project_type,expected_content",
    [
        ("package", "make test"),
        ("cli", "make run"),
    ],
)
def test_readme_content(baked_project, project_type, expected_content):
    """Test that README contains project-type-specific instructions."""
    result = baked_project(
        project_name="awesome-project",
        project_description="An awesome test project",
        project_type=project_type,
    )
    readme = result.project_path / "README.md"

    assert readme.exists()
    assert file_contains_text(str(readme), "awesome-project")
    assert file_contains_text(
        str(readme), expected_content
    ), f"README should contain '{expected_content}' for {project_type}"


# ============================================================================
# Integration Tests - Feature Combinations
# ============================================================================


@pytest.mark.parametrize("project_type", ["package", "cli"])
@pytest.mark.parametrize(
    "features",
    [
        {"github_actions": "y", "mkdocs": "y", "codecov": "y"},  # All features
        {"github_actions": "y", "mkdocs": "n", "codecov": "n"},  # CI only
        {"github_actions": "n", "mkdocs": "y", "codecov": "n"},  # Docs only
        {"github_actions": "n", "mkdocs": "n", "codecov": "n"},  # Minimal
    ],
    ids=["all-features", "ci-only", "docs-only", "minimal"],
)
def test_feature_combinations(baked_project, project_type, features):
    """Test that various feature combinations work with both project types."""
    result = baked_project(project_type=project_type, **features)

    # Verify features are correctly enabled/disabled
    assert (result.project_path / ".github").is_dir() == (features["github_actions"] == "y")
    assert (result.project_path / "docs").is_dir() == (features["mkdocs"] == "y")
    assert (result.project_path / "mkdocs.yml").is_file() == (features["mkdocs"] == "y")

    # Verify basic structure is always present
    assert (result.project_path / "pyproject.toml").is_file()
    assert (result.project_path / "Makefile").is_file()
    assert (result.project_path / ".pre-commit-config.yaml").is_file()
    assert (result.project_path / "tests").is_dir()


# ============================================================================
# Project Type Tests (CLI)
# ============================================================================


@pytest.mark.parametrize(
    "project_type,expected_files,not_expected",
    [
        ("package", ["{PACKAGE_NAME_PLACEHOLDER}/example.py"], ["{PACKAGE_NAME_PLACEHOLDER}/cli.py"]),
        ("cli", ["{PACKAGE_NAME_PLACEHOLDER}/cli.py"], ["{PACKAGE_NAME_PLACEHOLDER}/example.py"]),
    ],
)
def test_project_type_files(baked_project, project_type, expected_files, not_expected):
    """Test correct files exist for each project type."""
    result = baked_project(project_type=project_type)

    for file_path in expected_files:
        actual_path = file_path.replace("{PACKAGE_NAME_PLACEHOLDER}", result.project_path.name.replace("-", "_"))
        full_path = result.project_path / actual_path
        assert full_path.exists(), f"Expected {file_path} for {project_type}"

    for file_path in not_expected:
        actual_path = file_path.replace("{PACKAGE_NAME_PLACEHOLDER}", result.project_path.name.replace("-", "_"))
        full_path = result.project_path / actual_path
        assert not full_path.exists(), f"Did not expect {file_path} for {project_type}"


@pytest.mark.parametrize(
    "project_type,should_have_cli_deps",
    [
        ("cli", True),
        ("package", False),
    ],
)
def test_cli_dependencies(baked_project, project_type, should_have_cli_deps):
    """Test CLI dependencies are present only in CLI projects."""
    result = baked_project(project_type=project_type)
    pyproject = result.project_path / "pyproject.toml"

    has_typer = file_contains_text(str(pyproject), "typer")
    has_rich = file_contains_text(str(pyproject), "rich")

    assert has_typer == should_have_cli_deps, f"typer dependency for {project_type}"
    assert has_rich == should_have_cli_deps, f"rich dependency for {project_type}"


@pytest.mark.parametrize(
    "project_type,has_scripts",
    [
        ("package", False),
        ("cli", True),
    ],
)
def test_cli_entry_point(baked_project, project_type, has_scripts):
    """Test CLI projects have entry point configuration."""
    result = baked_project(project_type=project_type)
    pyproject = result.project_path / "pyproject.toml"

    has_section = file_contains_text(str(pyproject), "[project.scripts]")
    assert has_section == has_scripts


@pytest.mark.parametrize(
    "project_type,should_have_run_target",
    [
        ("cli", True),
        ("package", False),
    ],
)
def test_makefile_run_target(baked_project, project_type, should_have_run_target):
    """Test run target is present only in CLI projects."""
    result = baked_project(project_type=project_type)
    makefile = result.project_path / "Makefile"

    has_run_target = file_contains_text(str(makefile), "run: ## Run the CLI application")
    assert has_run_target == should_have_run_target, f"run target for {project_type}"


@pytest.mark.parametrize(
    "project_type,expected_in_tests",
    [
        ("cli", "from typer.testing import CliRunner"),
        ("package", "@pytest.mark.parametrize"),
    ],
)
def test_project_type_test_content(baked_project, project_type, expected_in_tests):
    """Test that generated test files contain type-appropriate content."""
    result = baked_project(project_type=project_type)
    test_file = result.project_path / "tests" / "test_example.py"

    assert test_file.exists()
    assert file_contains_text(
        str(test_file), expected_in_tests
    ), f"Test file should contain '{expected_in_tests}' for {project_type}"


@pytest.mark.parametrize("project_type", ["package", "cli"])
def test_project_type_with_pytest(baked_project, project_type):
    """Test that both project types can run their own test suites."""
    result = baked_project(project_type=project_type, _needs_install=True)

    # Run the tests (environment already installed by hook)
    with run_within_dir(str(result.project_path)):
        assert subprocess.check_call(shlex.split("uv run pytest -v")) == 0
