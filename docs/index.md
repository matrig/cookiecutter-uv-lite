<style>
  .md-typeset h1,
  .md-content__button {
    display: none;
  }
</style>

---

A lightweight, modern Python project template using uv for blazing-fast dependency management. It supports the following features:

- [uv](https://docs.astral.sh/uv/) for dependency management
- Code quality with [ruff](https://github.com/charliermarsh/ruff), [mypy](https://mypy.readthedocs.io/en/stable/), [deptry](https://github.com/fpgmaas/deptry/) and [prettier](https://prettier.io/)
- Testing with [pytest](https://docs.pytest.org/en/7.1.x/)
- Documentation with [MkDocs](https://www.mkdocs.org/)
- Compatibility testing for multiple versions of Python with [tox-uv](https://github.com/tox-dev/tox-uv)
- **GitHub Actions CI/CD** with automated testing, documentation deployment, and security scanning
- **Enterprise GitHub support** with SSH-first authentication

## Quickstart

On your local machine, navigate to the directory in which you want to create a project directory, and run the following command:

```bash
uvx cookiecutter https://github.com/matrig/cookiecutter-uv-lite.git
```

or if you don't have `uv` installed yet:

```bash
pip install cookiecutter
cookiecutter https://github.com/matrig/cookiecutter-uv-lite.git
```

Follow the prompts to configure your project. You'll be asked about:

- **github_actions** [y/n]: Enable GitHub Actions CI/CD workflows
- **codecov** [y/n]: Enable Codecov integration for coverage reporting
- **mkdocs** [y/n]: Include MkDocs documentation setup
- **git_repo** [y/n]: Initialize git repository and optionally create remote

Once completed, a new directory containing your project will be created. Then navigate into your newly created project directory and follow the instructions in the `README.md` to complete the setup of your project.

## GitHub Actions Features

When you enable GitHub Actions (`github_actions: y`), your generated project gets enterprise-grade CI/CD:

### 🚀 **Continuous Integration**

- Multi-Python testing (3.9-3.13) across Ubuntu, macOS, and Windows
- Automated code quality checks (ruff linting, formatting, mypy type checking)
- Coverage reporting with optional Codecov integration

### 📚 **Documentation Deployment**

- Automatic deployment to GitHub Pages when you push to main
- Seamless integration with MkDocs if enabled

### 🔒 **Security Scanning**

- CodeQL analysis for security vulnerabilities
- Dependency scanning with Safety
- Weekly automated security checks

### 📈 **Professional Benefits**

- ✅ Prevents broken code from being merged
- ✅ Maintains high code quality standards
- ✅ Automatically keeps documentation up-to-date
- ✅ Monitors for security issues
- ✅ Works with GitHub.com and GitHub Enterprise

### Acknowledgements

This project is based on <https://github.com/patrickmineault/true-neutral-cookiecutter> and <https://github.com/fpgmaas/cookiecutter-uv>.
