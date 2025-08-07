# Tutorial

This page contains a complete tutorial on how to create your project.

## Step 1: Install uv

To start, we will need to install `uv`. The instructions to install uv can be found
[here](https://docs.astral.sh/uv/#getting-started). For MacOS or Linux;

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Step 2: Generate your project

On your local machine, navigate to the directory in which you want to
create a project directory, and run the following command:

```bash
uvx cookiecutter https://github.com/matrig/minicookiecutter.git
```

For an explanation of the prompt arguments, see
[Prompt Arguments](prompt_arguments.md).

## Step 3: Set up your Github repository

Create an empty [new repository](https://github.com/new) on Github. Give
it a name that only contains alphanumeric characters and optionally `-`.

## Step 4: Upload your project to Github

Run the following commands:

```bash
cd {{cookiecutter.project_name}}
git init -b main
git add .
git commit -m "Init commit"
git remote add origin git@github.com:{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}.git
git push -u origin main
```

### Step 5: Set Up Your Development Environment

Install the environment with:

```bash
make install
```

This will generate the `uv.lock` file
``

### 6. Commit the changes

Now we commit the changes made by the two steps above to the repository:

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

## Step 7: Enable your documentation

To enable your documentation on GitHub, first navigate to `Settings > Actions > General` in your repository, and under `Workflow permissions` select `Read and write permissions`.

Then navigate to `Settings > Code and Automation > Pages`. If you succesfully created a new release,
you should see a notification saying ` Your site is ready to be published at https://{{cookiecutter.author_github_handle}}.github.io/{{cookiecutter.project_name}}/`.

To finalize deploying your documentation, under `Source`, select the branch `gh-pages`.

## Step 8: You're all set!

That's it! I hope this repository saved you a lot of manual configuration. If you have any improvement suggestions, feel
free to raise an issue or open a PR on Github!
