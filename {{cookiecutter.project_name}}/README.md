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

### 2. Commit the changes

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
