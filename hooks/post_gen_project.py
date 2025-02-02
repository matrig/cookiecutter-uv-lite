#!/usr/bin/env python
from __future__ import annotations

import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

HELP = """
The project {{cookiecutter.project_name}} has been created!

If you have not done so already:

1. Create a repository on GitHub with the same name as this project:

```bash
cd {{cookiecutter.project_name}}
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@{{cookiecutter.git_server}}:{{cookiecutter.author_username}}/{{cookiecutter.project_name}}.git
git push -u origin main
```

2. Install the environment:

```bash
make install
```

Have fun!
"""


def remove_file(filepath: str) -> None:
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(filepath: str) -> None:
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == "__main__":
    if "{{cookiecutter.mkdocs}}" != "y":
        remove_dir("docs")
        remove_file("mkdocs.yml")
    print(HELP)
