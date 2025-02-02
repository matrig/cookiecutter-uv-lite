# minicookiecutter

---

[![Build status](https://img.shields.io/github/actions/workflow/status/matrig/minicookiecutter/main.yml?branch=main)](https://github.com/matrig/minicookiecutter/actions/workflows/main.yml?query=branch%3Amain)
[![Supported Python versions](https://img.shields.io/badge/python-3.9_%7C_3.10_%7C_3.11_%7C_3.12_%7C_3.13-blue?labelColor=grey&color=blue)](https://github.com/matrig/minicookiecutter/blob/main/pyproject.toml)
[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://matrig.github.io/minicookiecutter/)

A minimalist cookiecutter for small projects using `uv` for dependency management.
It supports the following features:

- [uv](https://docs.astral.sh/uv/) for dependency management
- Code quality with [ruff](https://github.com/charliermarsh/ruff), [mypy](https://mypy.readthedocs.io/en/stable/), [deptry](https://github.com/fpgmaas/deptry/) and [prettier](https://prettier.io/)
- Testing with [pytest](https://docs.pytest.org/en/7.1.x/)
- Documentation with [MkDocs](https://www.mkdocs.org/)
- Compatibility testing for multiple versions of Python with [tox-uv](https://github.com/tox-dev/tox-uv)

---

<p align="center">
  <a href="https://matrig.github.io/minicookiecutter/">Documentation</a>
</p>

---

## Quickstart

On your local machine, navigate to the directory in which you want to create a project directory, and run the following command:

```bash
uvx cookiecutter https://github.com/matrig/minicookiecutter.git
```

## Acknowledgements

This project is based on <https://github.com/patrickmineault/true-neutral-cookiecutter> and <https://github.com/fpgmaas/cookiecutter-uv>.
