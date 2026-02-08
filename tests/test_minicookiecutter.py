from __future__ import annotations

import shlex
import subprocess
from unittest.mock import patch

import pytest

from tests.utils import file_contains_text, run_within_dir

# ============================================================================
# Basic Project Generation Tests
# ============================================================================


def test_bake_project(baked_project):
    """Test basic project baking with custom name."""
    result = baked_project(project_name="my-project")
    assert result.exception is None
    assert result.project_path.name == "my-project"


@pytest.mark.slow
def test_using_pytest(baked_project):
    """Test that generated project can run its own tests."""
    result = baked_project()

    # Install the uv environment and run the tests
    with run_within_dir(str(result.project_path)):
        assert subprocess.check_call(shlex.split("uv sync")) == 0
        assert subprocess.check_call(shlex.split("uv run make test")) == 0


def test_cli_main():
    """Test the CLI main function."""
    from minicookiecutter.cli import main

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


@pytest.mark.parametrize(
    "file_path,expected_contents",
    [
        (".pre-commit-config.yaml", ["ruff", "prettier", "pre-commit-hooks"]),
        ("pyproject.toml", ["ruff", "mypy", "pytest"]),
        ("tox.ini", ["[tox]"]),
    ],
)
def test_config_file_content(baked_project, file_path, expected_contents):
    """Test that configuration files contain expected content."""
    result = baked_project()
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


@pytest.mark.parametrize(
    "project_name,expected_package_name",
    [
        ("my-project", "my_project"),
        ("my-cool-app", "my_cool_app"),
        ("test-123", "test_123"),
        ("a-b-c-d", "a_b_c_d"),
    ],
)
def test_package_name_derivation(baked_project, project_name, expected_package_name):
    """Test that package names are correctly derived from project names."""
    result = baked_project(project_name=project_name)

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


def test_pyproject_metadata(baked_project):
    """Test that pyproject.toml contains correct project metadata."""
    result = baked_project(
        project_name="test-app",
        project_description="A test application",
    )
    pyproject = result.project_path / "pyproject.toml"

    assert file_contains_text(str(pyproject), 'name = "test-app"')
    assert file_contains_text(str(pyproject), "A test application")


def test_readme_content(baked_project):
    """Test that README contains project information."""
    result = baked_project(
        project_name="awesome-project",
        project_description="An awesome test project",
    )
    readme = result.project_path / "README.md"

    assert readme.exists()
    assert file_contains_text(str(readme), "awesome-project")


# ============================================================================
# Integration Tests - Feature Combinations
# ============================================================================


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
def test_feature_combinations(baked_project, features):
    """Test that various feature combinations work correctly together."""
    result = baked_project(**features)

    # Verify features are correctly enabled/disabled
    assert (result.project_path / ".github").is_dir() == (features["github_actions"] == "y")
    assert (result.project_path / "docs").is_dir() == (features["mkdocs"] == "y")
    assert (result.project_path / "mkdocs.yml").is_file() == (features["mkdocs"] == "y")

    # Verify basic structure is always present
    assert (result.project_path / "pyproject.toml").is_file()
    assert (result.project_path / "Makefile").is_file()
    assert (result.project_path / ".pre-commit-config.yaml").is_file()
    assert (result.project_path / "tests").is_dir()
