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


@pytest.mark.parametrize("project_type", ["package", "cli", "notebooks"])
def test_bake_project(baked_project, project_type):
    """Test basic project baking with custom name for all project types."""
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


@pytest.mark.parametrize("project_type", ["package", "cli", "notebooks"])
@pytest.mark.parametrize(
    "file_path,expected_contents",
    [
        (".pre-commit-config.yaml", ["ruff", "prettier", "pre-commit-hooks"]),
        ("pyproject.toml", ["ruff", "mypy", "pytest"]),
        ("tox.ini", ["[tox]"]),
    ],
)
def test_config_file_content(baked_project, project_type, file_path, expected_contents):
    """Test that configuration files contain expected content for all project types."""
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


@pytest.mark.parametrize("project_type", ["package", "cli", "notebooks"])
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
    """Test that package names are correctly derived from project names for all types."""
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


@pytest.mark.parametrize("project_type", ["package", "cli", "notebooks"])
def test_pyproject_metadata(baked_project, project_type):
    """Test that pyproject.toml contains correct project metadata for all types."""
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
        ("notebooks", "make jupyter"),
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


@pytest.mark.parametrize("project_type", ["package", "cli", "notebooks"])
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
    """Test that various feature combinations work with all project types."""
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
        (
            "package",
            ["{PACKAGE_NAME_PLACEHOLDER}/example.py"],
            ["{PACKAGE_NAME_PLACEHOLDER}/cli.py", "notebooks", "data"],
        ),
        ("cli", ["{PACKAGE_NAME_PLACEHOLDER}/cli.py"], ["{PACKAGE_NAME_PLACEHOLDER}/example.py", "notebooks", "data"]),
        (
            "notebooks",
            ["{PACKAGE_NAME_PLACEHOLDER}/utils.py", "notebooks", "data"],
            ["{PACKAGE_NAME_PLACEHOLDER}/example.py", "{PACKAGE_NAME_PLACEHOLDER}/cli.py"],
        ),
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


@pytest.mark.parametrize("project_type", ["package", "cli", "notebooks"])
def test_make_check_passes(baked_project, project_type):
    """Test that make check passes for all generated project types."""
    result = baked_project(project_type=project_type, _needs_install=True)

    # Run the full code quality checks (environment already installed by hook)
    with run_within_dir(str(result.project_path)):
        assert subprocess.check_call(shlex.split("uv run make check")) == 0


@pytest.mark.parametrize("project_type", ["package", "cli", "notebooks"])
def test_make_build_passes(baked_project, project_type):
    """Test that make build successfully creates a wheel for all project types."""
    result = baked_project(project_type=project_type, _needs_install=True)

    # Build the wheel distribution (environment already installed by hook)
    with run_within_dir(str(result.project_path)):
        assert subprocess.check_call(shlex.split("uv run make build")) == 0
        # Verify wheel was created
        dist_dir = result.project_path / "dist"
        assert dist_dir.exists()
        wheel_files = list(dist_dir.glob("*.whl"))
        assert len(wheel_files) == 1, "Should create exactly one wheel file"


# ============================================================================
# Notebooks Project Type Tests
# ============================================================================


def test_notebooks_directory_structure(baked_project):
    """Test that notebooks project has correct directory structure."""
    result = baked_project(project_type="notebooks")

    # Verify notebooks directory exists with sample notebooks
    notebooks_dir = result.project_path / "notebooks"
    assert notebooks_dir.is_dir()
    assert (notebooks_dir / "README.md").is_file()
    assert (notebooks_dir / "01-exploratory.ipynb").is_file()
    assert (notebooks_dir / "02-visualization.ipynb").is_file()

    # Verify data directory exists
    data_dir = result.project_path / "data"
    assert data_dir.is_dir()
    assert (data_dir / "README.md").is_file()
    assert (data_dir / ".gitkeep").is_file()


def test_notebooks_dependencies(baked_project):
    """Test that notebooks project has correct dependencies."""
    result = baked_project(project_type="notebooks")
    pyproject = result.project_path / "pyproject.toml"

    # Check main dependencies
    assert file_contains_text(str(pyproject), "jupyterlab>=4.0.0")
    assert file_contains_text(str(pyproject), "pandas>=2.0.0")
    assert file_contains_text(str(pyproject), "numpy>=1.24.0")
    assert file_contains_text(str(pyproject), "matplotlib>=3.7.0")
    assert file_contains_text(str(pyproject), "seaborn>=0.12.0")
    assert file_contains_text(str(pyproject), "ipywidgets>=8.0.0")

    # Check dev dependencies
    assert file_contains_text(str(pyproject), "nbval>=0.10.0")
    assert file_contains_text(str(pyproject), "nbconvert>=7.0.0")

    # Verify jupyterlab is not in dev dependencies (it's in main dependencies)
    pyproject_content = pyproject.read_text()
    # Check that jupyterlab appears before [dependency-groups]
    deps_section_idx = pyproject_content.find("dependencies = [")
    dev_section_idx = pyproject_content.find("[dependency-groups]")
    jupyterlab_idx = pyproject_content.find("jupyterlab>=4.0.0")
    assert deps_section_idx < jupyterlab_idx < dev_section_idx


def test_notebooks_makefile_targets(baked_project):
    """Test that notebooks project has correct Makefile targets."""
    result = baked_project(project_type="notebooks")
    makefile = result.project_path / "Makefile"

    # Check notebooks-specific targets exist
    assert file_contains_text(str(makefile), "jupyter: ## Start JupyterLab server")
    assert file_contains_text(str(makefile), "jupyter-notebook: ## Start Jupyter Notebook")
    assert file_contains_text(str(makefile), "test-notebooks: ## Test notebooks execute without errors")

    # Verify they use correct commands
    assert file_contains_text(str(makefile), "uv run jupyter lab")
    assert file_contains_text(str(makefile), "uv run jupyter notebook")
    assert file_contains_text(str(makefile), "pytest --nbval notebooks/")

    # CLI-specific target should not exist
    assert not file_contains_text(str(makefile), "run: ## Run the CLI application")


def test_notebooks_utils_module(baked_project):
    """Test that notebooks project has utils.py with data science helpers."""
    result = baked_project(project_type="notebooks", project_name="my-project")
    utils_file = result.project_path / "my_project" / "utils.py"

    assert utils_file.is_file()
    assert file_contains_text(str(utils_file), "def load_sample_data()")
    assert file_contains_text(str(utils_file), "def setup_plotting_style()")
    assert file_contains_text(str(utils_file), "pd.DataFrame")


def test_notebooks_gitignore_entries(baked_project):
    """Test that notebooks project has notebook-specific gitignore entries."""
    result = baked_project(project_type="notebooks")
    gitignore = result.project_path / ".gitignore"

    # Check notebook-specific patterns
    assert file_contains_text(str(gitignore), "*.ipynb_checkpoints")
    assert file_contains_text(str(gitignore), "*/.ipynb_checkpoints/*")
    assert file_contains_text(str(gitignore), ".jupyter/")
    assert file_contains_text(str(gitignore), "*.pkl")
    assert file_contains_text(str(gitignore), "*.pickle")


def test_notebooks_readme_instructions(baked_project):
    """Test that notebooks README contains appropriate instructions."""
    result = baked_project(project_type="notebooks", project_name="data-project")
    readme = result.project_path / "README.md"

    assert file_contains_text(str(readme), "make jupyter")
    assert file_contains_text(str(readme), "01-exploratory.ipynb")
    assert file_contains_text(str(readme), "02-visualization.ipynb")
    assert file_contains_text(str(readme), "make test-notebooks")


def test_notebooks_sample_notebooks_content(baked_project):
    """Test that sample notebooks contain expected content."""
    result = baked_project(project_type="notebooks", project_name="test-proj")

    # Check exploratory notebook
    exploratory_nb = result.project_path / "notebooks" / "01-exploratory.ipynb"
    assert file_contains_text(str(exploratory_nb), "load_sample_data")
    assert file_contains_text(str(exploratory_nb), "from test_proj.utils import")
    assert file_contains_text(str(exploratory_nb), "Exploratory Data Analysis")
    assert file_contains_text(str(exploratory_nb), "df.describe()")
    assert file_contains_text(str(exploratory_nb), "df.groupby")

    # Check visualization notebook
    viz_nb = result.project_path / "notebooks" / "02-visualization.ipynb"
    assert file_contains_text(str(viz_nb), "matplotlib.pyplot")
    assert file_contains_text(str(viz_nb), "seaborn")
    assert file_contains_text(str(viz_nb), "setup_plotting_style")
    assert file_contains_text(str(viz_nb), "from test_proj.utils import")
    assert file_contains_text(str(viz_nb), "Data Visualization")


def test_make_test_notebooks_passes(baked_project):
    """Test that make test-notebooks successfully executes notebooks with nbval."""
    result = baked_project(project_type="notebooks", _needs_install=True)

    # Test that notebooks execute without errors (environment already installed by hook)
    with run_within_dir(str(result.project_path)):
        assert subprocess.check_call(shlex.split("uv run make test-notebooks")) == 0


@pytest.mark.parametrize(
    "project_type,should_have_notebooks_deps",
    [
        ("notebooks", True),
        ("package", False),
        ("cli", False),
    ],
)
def test_notebooks_dependencies_only_in_notebooks_type(baked_project, project_type, should_have_notebooks_deps):
    """Test that notebooks dependencies are only in notebooks projects."""
    result = baked_project(project_type=project_type)
    pyproject = result.project_path / "pyproject.toml"

    has_pandas = file_contains_text(str(pyproject), "pandas>=")
    has_matplotlib = file_contains_text(str(pyproject), "matplotlib>=")
    has_nbval = file_contains_text(str(pyproject), "nbval>=")

    assert has_pandas == should_have_notebooks_deps, f"pandas dependency for {project_type}"
    assert has_matplotlib == should_have_notebooks_deps, f"matplotlib dependency for {project_type}"
    assert has_nbval == should_have_notebooks_deps, f"pytest-nbval dependency for {project_type}"
