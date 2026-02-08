# cookiecutter-uv-lite

---

[![Build status](https://img.shields.io/github/actions/workflow/status/matrig/cookiecutter-uv-lite/main.yml?branch=main)](https://github.com/matrig/cookiecutter-uv-lite/actions/workflows/main.yml?query=branch%3Amain)
[![Supported Python versions](https://img.shields.io/badge/python-3.9_%7C_3.10_%7C_3.11_%7C_3.12_%7C_3.13-blue?labelColor=grey&color=blue)](https://github.com/matrig/cookiecutter-uv-lite/blob/main/pyproject.toml)
[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://matrig.github.io/cookiecutter-uv-lite/)

A lightweight, modern Python project template using `uv` for blazing-fast dependency management.

**Choose your project type:**

- 📦 **Package**: Python libraries and packages
- 🚀 **CLI**: Command-line applications with [Typer](https://typer.tiangolo.com/) and [Rich](https://rich.readthedocs.io/)

**Features:**

- [uv](https://docs.astral.sh/uv/) for dependency management
- Code quality with [ruff](https://github.com/charliermarsh/ruff), [mypy](https://mypy.readthedocs.io/en/stable/), [deptry](https://github.com/fpgmaas/deptry/) and [prettier](https://prettier.io/)
- Testing with [pytest](https://docs.pytest.org/en/7.1.x/)
- Documentation with [MkDocs](https://www.mkdocs.org/)
- Compatibility testing for multiple versions of Python with [tox-uv](https://github.com/tox-dev/tox-uv)
- **GitHub Actions CI/CD** with automated testing, documentation deployment, and security scanning
- **Enterprise GitHub support** with SSH-first authentication

---

<p align="center">
  <a href="https://matrig.github.io/cookiecutter-uv-lite/">Documentation</a>
</p>

---

## Quickstart

On your local machine, navigate to the directory in which you want to create a project directory, and run the following command:

```bash
uvx cookiecutter https://github.com/matrig/cookiecutter-uv-lite.git
```

You'll be prompted to configure your project (12 questions):

1. **project_type**: Choose between `package` (library) or `cli` (command-line app)
2. **project_name**: Your project name (e.g., `my-awesome-project`)
3. **project_description**: Short description of your project
4. **author**: Your name
5. **author_email**: Your email
6. **author_username**: Your GitHub username
7. **git_repo** [y/n]: Initialize git repository and optionally create remote on GitHub
8. **git_server**: GitHub server (default: `github.com`, or your enterprise domain)
9. **private_repo** [y/n]: Create private repository
10. **mkdocs** [y/n]: Include MkDocs documentation
11. **github_actions** [y/n]: Enable GitHub Actions CI/CD
12. **codecov** [y/n]: Enable Codecov integration

### Project Types

**📦 Package** - Python libraries and packages

- Includes example module with function
- Standard package structure
- Ready for PyPI publishing

**🚀 CLI** - Command-line applications

- Built with [Typer](https://typer.tiangolo.com/) (modern CLI framework)
- Styled output with [Rich](https://rich.readthedocs.io/)
- Executable entry point configured
- `make run` command with argument support

## GitHub Actions Features

When you enable GitHub Actions (`github_actions: y`), your generated project includes:

### 🚀 **Continuous Integration (CI)**

- **Multi-Python testing**: Automatically tests your code on Python 3.9-3.13
- **Multi-OS testing**: Tests on Ubuntu, macOS, and Windows
- **Code quality checks**: Automated linting (ruff), formatting, and type checking (mypy)
- **Coverage reporting**: Optional integration with Codecov

### 📚 **Documentation Deployment**

- **Auto-deploy to GitHub Pages**: Documentation automatically updates when you push to main
- **MkDocs integration**: Works seamlessly if you enable MkDocs

### 🔒 **Security Scanning**

- **CodeQL analysis**: GitHub's native security scanning
- **Dependency scanning**: Automated vulnerability detection with Safety
- **Scheduled security checks**: Weekly automated scans

### 📈 **Professional Setup**

Your generated project gets enterprise-grade CI/CD that:

- ✅ Prevents bad code from being merged
- ✅ Automatically deploys documentation
- ✅ Monitors for security vulnerabilities
- ✅ Works with both GitHub.com and GitHub Enterprise

## Acknowledgements

This project is based on <https://github.com/patrickmineault/true-neutral-cookiecutter> and <https://github.com/fpgmaas/cookiecutter-uv>.
