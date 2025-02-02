# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

- **Git repository**: <https://{{cookiecutter.git_server}}/{{cookiecutter.author_username}}/{{cookiecutter.project_name}}/>

{% if cookiecutter.git_server == "github.com" %}
- **Documentation** <https://{{cookiecutter.author_username}}.github.io/{{cookiecutter.project_name}}/>
{% endif %}

## Getting started with your project

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@{{cookiecutter.git_server}}:{{cookiecutter.author_username}}/{{cookiecutter.project_name}}.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!

For activating the automatic documentation with MkDocs, see [here](https://matrig.github.io/minicookiecutter/features/mkdocs/#enabling-the-documentation-on-github).


---

Repository initiated with [matrig/minicookiecutter](https://github.com/matrig/minicookiecutter).
