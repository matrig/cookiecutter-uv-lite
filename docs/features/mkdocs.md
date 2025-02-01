# Documentation with MkDocs

If `mkdocs` is set to `"y"`, documentation of your project is automatically added using
[MkDocs](https://www.mkdocs.org/).
The documentation can then be  deployed to your `gh-pages` branch, and made available at
`https://<github_handle>.github.io/<project_name>/` by using the command
```bash
make docs-deploy
```
(which will deploy the project pages to a branch called `gh-pages`), and following the instructions below on how to enable the documentation on GitHub.

To view the documentation locally, simply run

```bash
make docs
```

This command will generate and build your documentation, and start the server locally so you can access it at
<http://localhost:8000>.

## Enabling the documentation on GitHub

To enable your documentation on GitHub, in your repository, navigate to `Settings > Code and Automation > Pages`.
Then, under `Branch`, select the branch `gh-pages` and `/(root)`. Your documentation should then be live within a few minutes.

## Documenting docstrings

The generated project also converts all your docstrings into legible documentation. By default, the project is configured to work with
[google](https://google.github.io/styleguide/pyguide.html) style docstrings.

An example of a Google style docstring:

```python
def function_with_pep484_type_annotations(param1: int, param2: str) -> bool:
"""Example function with PEP 484 type annotations.

Args:
    param1: The first parameter.
    param2: The second parameter.

Returns:
    The return value. True for success, False otherwise.
```

For more examples, see
[here](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
