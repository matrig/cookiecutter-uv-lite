from __future__ import annotations

import os
import shlex
import subprocess

from tests.utils import file_contains_text, run_within_dir


def test_bake_project(cookies):
    result = cookies.bake(extra_context={"project_name": "my-project"})

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == "my-project"
    assert result.project_path.is_dir()


def test_using_pytest(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake()

        # Assert that project was created.
        assert result.exit_code == 0
        assert result.exception is None
        assert result.project_path.name == "my-project"
        assert result.project_path.is_dir()

        # Install the uv environment and run the tests.
        with run_within_dir(str(result.project_path)):
            assert subprocess.check_call(shlex.split("uv sync")) == 0
            assert subprocess.check_call(shlex.split("uv run make test")) == 0


def test_mkdocs(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"mkdocs": "y"})
        assert result.exit_code == 0
        assert file_contains_text(f"{result.project_path}/Makefile", "docs:")
        assert os.path.isdir(f"{result.project_path}/docs")


def test_not_mkdocs(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"mkdocs": "n"})
        assert result.exit_code == 0
        assert not file_contains_text(f"{result.project_path}/Makefile", "docs:")
        assert not os.path.isdir(f"{result.project_path}/docs")


def test_tox(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake()
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/tox.ini")
        assert file_contains_text(f"{result.project_path}/tox.ini", "[tox]")
