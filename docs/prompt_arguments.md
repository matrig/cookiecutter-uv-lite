# Prompt arguments

When running the command `ccp` a prompt will start which enables you to configure your repository. The prompt values and their explanation are as follows:

---

**author**

Your full name.

**author_email**

Your email address associated with your github account.

**author_username**

Your github handle, i.e. `<handle>` in `https://github.com/<handle>`.

**project_name**

Your project name. Should be equal to the name of your repository
and it should only contain alphanumeric characters and `-`'s.

**package_name**

The package name, will default to the `project_name` with all `-`'s
replaced with `_`. This will be how you import your code later, e.g.

```python
from <package_nem> import foo
```

Note: You can set `package_name` to `"src"` to place the Python module inside a `src` directory.

**project_description**

A short description of your project.

**git_repo**

`"y"` or `"n"`. Whether you want to create a local git repo for the project.

**git_server**

In case you want to use another git service than github, you can specify it here. The default is `github.com`.

**mkdocs**

`"y"` or `"n"`. Adds [MkDocs](https://www.mkdocs.org/)
documentation to your project. This includes automatically parsing your docstrings and adding them to the documentation. Documentation will be deployed to the `gh-pages` branch.

**github_actions**

`"y"` or `"n"`. Adds GitHub Actions CI/CD workflows to your project. When enabled, your project gets:

- **Continuous Integration**: Automated testing across Python 3.9-3.13 and multiple operating systems (Ubuntu, macOS, Windows)
- **Code Quality Checks**: Automatic linting (ruff), formatting, and type checking (mypy)
- **Documentation Deployment**: Automatic deployment to GitHub Pages when MkDocs is also enabled
- **Security Scanning**: CodeQL analysis and dependency vulnerability scanning with weekly automated checks

This adds `pytest-cov>=4.0.0` to your dev dependencies for coverage reporting.

**codecov**

`"y"` or `"n"`. Enables [Codecov](https://codecov.io/) integration for coverage reporting. Only relevant if `github_actions` is also set to `"y"`. When enabled, your CI pipeline will automatically upload coverage reports to Codecov and provide coverage analysis on pull requests.

---
