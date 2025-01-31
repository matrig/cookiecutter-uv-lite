# Prompt arguments

When running the command `ccp` a prompt will start which enables you to configure your repository. The prompt values and their explanation are as follows:

---

**author**

Your full name.

**author_github_handle**

Your github handle, i.e. `<handle>` in `https://github.com/<handle>`

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

**mkdocs**

`"y"` or `"n"`. Adds [MkDocs](https://www.mkdocs.org/)
documentation to your project. This includes automatically parsing your docstrings and adding them to the documentation. Documentation will be deployed to the `gh-pages` branch.

---
