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
You can set up a remote git repository on {{cookiecutter.git_server}} later by:

1. Creating an empty repository named {{cookiecutter.project_name}} on {{cookiecutter.git_server}}
2. Then running the following commands:

>> cd {{cookiecutter.project_name}}
>> git remote add origin git@{{cookiecutter.git_server}}:{{cookiecutter.author_username}}/{{cookiecutter.project_name}}.git
>> git branch -M main
>> git push -u origin main

Note: This works with SSH authentication (no tokens needed if you have SSH keys set up).

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

        # Install pre-commit hooks:
        subprocess.run([get_exec_path("uv"), "run", "pre-commit", "install"], cwd=PROJECT_DIRECTORY, check=True)  # noqa: S603
    except subprocess.CalledProcessError as e:
        print(f"Error creating git repository: {e}")
        return False
    else:
        return True


def create_github_repo(username: str, repo_name: str, is_private: bool = False) -> bool:
    """Create GitHub repository using GitHub CLI if available, otherwise skip."""
    try:
        # Set up environment for GitHub CLI to use the correct host
        env = os.environ.copy()
        env["GH_HOST"] = "{{cookiecutter.git_server}}"

        # Determine visibility flag
        visibility_flag = "--private" if is_private else "--public"

        # Try using GitHub CLI (works with both github.com and enterprise)
        subprocess.run(  # noqa: S603
            [get_exec_path("gh"), "repo", "create", repo_name, visibility_flag],
            env=env,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        # GitHub CLI not available or failed
        print(f"GitHub CLI (gh) not available or failed. Please create repository '{repo_name}' manually.")
        return False
    else:
        return True


def add_remote_git_repo(use_ssh: bool = True) -> bool:
    """Add remote repository and push, preferring SSH authentication."""
    try:
        if use_ssh:
            remote_url = (
                "git@{{cookiecutter.git_server}}:{{cookiecutter.author_username}}/{{cookiecutter.project_name}}.git"
            )
        else:
            remote_url = (
                "https://{{cookiecutter.git_server}}/{{cookiecutter.author_username}}/{{cookiecutter.project_name}}.git"
            )

        subprocess.run([get_exec_path("git"), "remote", "add", "origin", remote_url], cwd=PROJECT_DIRECTORY, check=True)  # noqa: S603
        subprocess.run([get_exec_path("git"), "branch", "-M", "main"], cwd=PROJECT_DIRECTORY, check=True)  # noqa: S603

        # Try pushing with SSH first, fallback to HTTPS if it fails
        try:
            subprocess.run([get_exec_path("git"), "push", "-u", "origin", "main"], cwd=PROJECT_DIRECTORY, check=True)  # noqa: S603
        except subprocess.CalledProcessError:
            if use_ssh:
                print("SSH push failed, you may need to:")
                print("1. Add your SSH key to your GitHub account")
                print(
                    "2. Or run: git remote set-url origin https://{{cookiecutter.git_server}}/{{cookiecutter.author_username}}/{{cookiecutter.project_name}}.git"
                )
                print("3. Then manually push: git push -u origin main")
            return False
        else:
            return True

    except subprocess.CalledProcessError as e:
        print(f"Error setting up remote git repository: {e}")
        return False


if __name__ == "__main__":
    if "{{cookiecutter.mkdocs}}" != "y":
        remove_dir("docs")
        remove_file("mkdocs.yml")

    if "{{cookiecutter.github_actions}}" != "y":
        remove_dir(".github")

    # Create environment:
    print("Creating environment...")
    subprocess.run(["make", "install"], cwd=PROJECT_DIRECTORY, check=True)  # noqa: S603, S607

    # Create local git repository?
    if "{{cookiecutter.git_repo}}" == "y":
        local_repo_created = create_local_git_repo()
        if local_repo_created:
            print("Git repo was successfully created in {{cookiecutter.project_name}}")

    if "{{cookiecutter.git_repo}}" != "y" or not local_repo_created:
        print(HELP_LOCAL_REPO)

    if "{{cookiecutter.git_repo}}" == "y" and local_repo_created:
        # Create remote git repository?
        try:
            ask_remote_repo = (
                input(
                    "Do you want to create a remote git repository {{cookiecutter.project_name}} on {{cookiecutter.git_server}}? (y/n): "
                )
                .strip()
                .lower()
            )
        except EOFError:
            # Handle non-interactive environments (like automated testing)
            ask_remote_repo = "n"
            print("Non-interactive environment detected. Skipping remote repository creation.")

        remote_repo_created = False
        if ask_remote_repo == "y":
            # Determine repository visibility
            repo_is_private = "{{cookiecutter.private_repo}}" == "y"

            # Ask user interactively for repository visibility preference
            try:
                ask_private_repo = (
                    input(f"Should the repository be private? (y/n) [default: {'y' if repo_is_private else 'n'}]: ")
                    .strip()
                    .lower()
                )
                # Use user input if provided, otherwise use cookiecutter default
                if ask_private_repo in ["y", "n"]:
                    repo_is_private = ask_private_repo == "y"
            except EOFError:
                # Handle non-interactive environments
                print(
                    f"Non-interactive environment detected. Creating {'private' if repo_is_private else 'public'} repository."
                )

            # Try to create repository using GitHub CLI (works with both github.com and enterprise)
            github_repo_created = create_github_repo(
                "{{cookiecutter.author_username}}", "{{cookiecutter.project_name}}", repo_is_private
            )

            # Set up remote repository (preferring SSH)
            remote_repo_created = add_remote_git_repo(use_ssh=True)
            if remote_repo_created:
                print("Remote git repository was successfully created and set up on {{cookiecutter.git_server}}")

        if ask_remote_repo != "y" or not remote_repo_created:
            print(HELP_REMOTE_REPO)

    print(END_MESSAGE)
