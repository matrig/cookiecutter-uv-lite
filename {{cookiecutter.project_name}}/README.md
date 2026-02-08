{% set package_name = cookiecutter.project_name|lower|replace('-', '_') -%}
# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

- **Git repository**: <https://{{cookiecutter.git_server}}/{{cookiecutter.author_username}}/{{cookiecutter.project_name}}/>

{% if cookiecutter.git_server == "github.com" %}
- **Documentation** <https://{{cookiecutter.author_username}}.github.io/{{cookiecutter.project_name}}/>
{% endif %}

## Getting started with your project

### 1. Set Up Your Development Environment

Install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

{% if cookiecutter.project_type == 'cli' %}
### 2. Run Your CLI Application

Run the CLI with:

```bash
make run
# Or directly:
uv run {{cookiecutter.project_name}} --help
```

{% elif cookiecutter.project_type == 'notebooks' %}
### 2. Start JupyterLab

Launch JupyterLab:

```bash
make jupyter
```

Open the example notebooks in `notebooks/`:
- `01-exploratory.ipynb`: Data exploration examples
- `02-visualization.ipynb`: Plotting examples

Your reusable code goes in `{{ package_name }}/utils.py`. Run tests with:

```bash
make test
make test-notebooks  # Test that notebooks execute without errors
```

{% else %}
### 2. Start Development

Your package code is in `{{package_name}}/`. Run tests with:

```bash
make test
```

{% endif %}
### 3. Commit the changes

Commit changes to your repository with

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!

For activating the automatic documentation with MkDocs, see [here](https://matrig.github.io/minicookiecutter/features/mkdocs/#enabling-the-documentation-on-github).


---

Repository initiated with [matrig/minicookiecutter](https://github.com/matrig/minicookiecutter).
