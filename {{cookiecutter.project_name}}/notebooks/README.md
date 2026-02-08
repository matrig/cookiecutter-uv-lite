# Notebooks

{% set package_name = cookiecutter.project_name|lower|replace('-', '_') -%}
This directory contains Jupyter notebooks for data analysis and visualization.

## Notebook Organization

- `01-exploratory.ipynb`: Initial data exploration
- `02-visualization.ipynb`: Data visualization examples

## Running Notebooks

Start JupyterLab:

```bash
make jupyter
```

Or use:

```bash
uv run jupyter lab
```

## Best Practices

1. Keep notebooks focused and well-documented
2. Move reusable code to `{{ package_name }}/utils.py`
3. Use clear markdown cells to explain your analysis
4. Run notebooks top-to-bottom before committing
5. Test notebooks with: `make test-notebooks`
