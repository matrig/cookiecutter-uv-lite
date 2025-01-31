<style>
  .md-typeset h1,
  .md-content__button {
    display: none;
  }
</style>

---

This is a minimalistic Cookiecutter template that can be used to initiate a Python project. It supports the following features:

- [uv](https://docs.astral.sh/uv/) for dependency management
- Code quality with [ruff](https://github.com/charliermarsh/ruff), [mypy](https://mypy.readthedocs.io/en/stable/), [deptry](https://github.com/fpgmaas/deptry/) and [prettier](https://prettier.io/)
- Testing with [pytest](https://docs.pytest.org/en/7.1.x/)
- Documentation with [MkDocs](https://www.mkdocs.org/)
- Compatibility testing for multiple versions of Python with [tox-uv](https://github.com/tox-dev/tox-uv)


## Quickstart

On your local machine, navigate to the directory in which you want to create a project directory, and run the following command:

```bash
uvx cookiecutter https://github.com/matrig/minicookiecutter.git
```

or if you don't have `uv` installed yet:

```bash
pip install cookiecutter
cookiecutter https://github.com/matrig/minicookiecutter.git
```

Follow the prompts to configure your project. Once completed, a new directory containing your project will be created. Then navigate into your newly created project directory and follow the instructions in the `README.md` to complete the setup of your project.

### Acknowledgements

This project is based on <https://github.com/patrickmineault/true-neutral-cookiecutter> and <https://github.com/fpgmaas/cookiecutter-uv>.
