#!/usr/bin/env python
from __future__ import annotations

import os
import shutil
import subprocess

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

HELP_LOCAL_REPO = """
You can create a git repository later by creating an empty repository named {{cookiecutter.project_name}} on {{cookiecutter.git_server}}
and running the following commands
>> cd {{cookiecutter.project_name}}
>> git init -b main
>> git add .
>> git commit -m "Initial commit"
"""

HELP_REMOTE_REPO = """
You can create a remote git repository on {{cookiecutter.git_server}} later by
creating an empty git repository named {{cookiecutter.project_name}} on {{cookiecutter.git_server}}
and then running the following commands
>> cd {{cookiecutter.project_name}}
>> git remote add origin git@{{cookiecutter.git_server}}:{{cookiecutter.author_username}}/{{cookiecutter.project_name}}.git
>> git push -u origin main
"""

END_MESSAGE = """
The project {{cookiecutter.project_name}} has been created!

Have fun!
"""


def remove_file(filepath: str) -> None:
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(filepath: str) -> None:
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, filepath))


def get_exec_path(executable: str) -> str:
    """Used to avoid ruff start-process-with-partial-path (S607)"""
    path = shutil.which(executable)
    if path is None:
        raise FileNotFoundError(executable)
    return path


def create_local_git_repo() -> bool:
    try:
        # Init repository:
        if os.path.isdir(PROJECT_DIRECTORY):
            subprocess.run([get_exec_path("git"), "init", "-b", "main"], cwd=PROJECT_DIRECTORY, check=True)  # noqa: S603

        # Configure git user name and email:
        author_name = "{{cookiecutter.author}}"
        author_email = "{{cookiecutter.author_email}}"
        subprocess.run([get_exec_path("git"), "config", "user.name", author_name], cwd=PROJECT_DIRECTORY, check=True)  # noqa: S603
        if author_email:
            subprocess.run(  # noqa: S603
                [get_exec_path("git"), "config", "user.email", author_email], cwd=PROJECT_DIRECTORY, check=True
            )

        # First commit:
        subprocess.run([get_exec_path("git"), "add", "."], cwd=PROJECT_DIRECTORY, check=True)  # noqa: S603
        subprocess.run([get_exec_path("git"), "commit", "-m", "Initial commit"], cwd=PROJECT_DIRECTORY, check=True)  # noqa: S603
    except subprocess.CalledProcessError as e:
        print(f"Error creating git repository: {e}")
        return False
    else:
        return True


def create_github_repo(username: str, repo_name: str) -> bool:
    try:
        subprocess.run(  # noqa: S603
            [
                get_exec_path("curl"),
                "-u",
                username,
                "https://api.github.com/user/repos",
                "-d",
                '{"name":' + f'"{repo_name}"' + "}",
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error creating GitHub repository: {e}")
        return False
    else:
        return True


def add_remote_git_repo(token: str) -> bool:
    try:
        if token:
            remote_url = f"https://{token}@{{cookiecutter.git_server}}/{{cookiecutter.author_username}}/{{cookiecutter.project_name}}.git"
        else:
            remote_url = (
                "git@{{cookiecutter.git_server}}:{{cookiecutter.author_username}}/{{cookiecutter.project_name}}.git"
            )
        subprocess.run([get_exec_path("git"), "remote", "add", "origin", remote_url], cwd=PROJECT_DIRECTORY, check=True)  # noqa: S603
        subprocess.run([get_exec_path("git"), "push", "-u", "origin", "main"], cwd=PROJECT_DIRECTORY, check=True)  # noqa: S603
    except subprocess.CalledProcessError as e:
        print(f"Error creating remote git repository: {e}")
        return False
    else:
        return True


if __name__ == "__main__":
    if "{{cookiecutter.mkdocs}}" != "y":
        remove_dir("docs")
        remove_file("mkdocs.yml")

    # Create environment:
    print("Creating environment...")
    subprocess.run(["make", "install"], cwd=PROJECT_DIRECTORY, check=True)  # noqa: S603, S607

    # Create local git repository?
    ask_local_repo = input("Do you want to create local git repository? (y/n): ").strip().lower()
    if ask_local_repo == "y":
        local_repo_created = create_local_git_repo()
        if local_repo_created:
            print("Git repo was sucessfully created in {{cookiecutter.project_name}}")

    if ask_local_repo != "y" or not local_repo_created:
        print(HELP_LOCAL_REPO)

    if ask_local_repo == "y" and local_repo_created:
        # Create remote git repository?
        ask_remote_repo = (
            input(
                "Do you want to create a remote git repository {{cookiecutter.project_name}} on {{cookiecutter.git_server}}? (y/n): "
            )
            .strip()
            .lower()
        )
        if ask_remote_repo == "y":
            if input("Do you have a GitHub token? (y/n): ").strip().lower() == "y":
                token = input("Enter your GitHub token: ")
            else:
                token = None

            github_repo_created = create_github_repo(
                "{{cookiecutter.author_username}}", "{{cookiecutter.project_name}}"
            )
            remote_repo_created = add_remote_git_repo(token)
            if remote_repo_created:
                print("Remote git repository was successfully created on {{cookiecutter.git_server}}")

        if ask_remote_repo != "y" or not remote_repo_created:
            print(HELP_REMOTE_REPO)

    print(END_MESSAGE)
