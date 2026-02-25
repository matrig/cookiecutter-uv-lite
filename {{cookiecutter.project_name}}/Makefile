PROJECT_NAME := {{cookiecutter.project_name}}

.PHONY: install
install: ## Install the virtual environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using uv"
	@uv sync
{% if cookiecutter.project_type == 'notebooks' %}
	@echo "🚀 Registering Jupyter kernel for this project"
	@uv run python -m ipykernel install --user --name $(PROJECT_NAME) --display-name "Python ($(PROJECT_NAME))"
{% endif %}
	@if [ -d .git ]; then uv run pre-commit install; fi

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking lock file consistency with 'pyproject.toml'"
	@uv lock --locked
	@if [ -d .git ]; then \
		echo "🚀 Linting code: Running pre-commit"; \
		uv run pre-commit run -a; \
	fi
	@echo "🚀 Static type checking: Running mypy"
	@uv run mypy

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@uv run python -m pytest --doctest-modules -n auto

{% if cookiecutter.project_type == 'cli' %}
# Capture arguments for 'make run'
ifeq (run,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

.PHONY: run
run: ## Run the CLI application (e.g., 'make run' or 'make run hello' or 'make run ARGS="hello --name Alice"')
	@uv run {{cookiecutter.project_name}} $(if $(ARGS),$(ARGS),$(if $(RUN_ARGS),$(RUN_ARGS),--help))

{% endif %}
{% if cookiecutter.project_type == 'notebooks' %}
.PHONY: jupyter
jupyter: ## Start JupyterLab server
	@echo "🚀 Starting JupyterLab..."
	@uv run jupyter lab

.PHONY: jupyter-notebook
jupyter-notebook: ## Start Jupyter Notebook (classic interface)
	@echo "🚀 Starting Jupyter Notebook..."
	@uv run jupyter notebook

.PHONY: test-notebooks
test-notebooks: ## Test notebooks execute without errors
	@echo "🚀 Testing notebooks with nbval..."
	@uv run pytest --nbval notebooks/

{% endif %}
.PHONY: build
build: clean-build ## Build wheel file
	@echo "🚀 Creating wheel file"
	@uvx --from build pyproject-build --installer uv

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@echo "🚀 Removing build artifacts"
	@uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

{%- if cookiecutter.mkdocs == "y" %}

.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@uv run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@uv run mkdocs serve

.PHONY: docs-deploy
docs-deploy: ## Deploy the documentation to a branch named gh-pages
	@uv run mkdocs gh-deploy --force

{%- endif %}

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.DEFAULT_GOAL := help
