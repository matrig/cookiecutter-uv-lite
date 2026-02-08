{% set package_name = cookiecutter.project_name|lower|replace('-', '_') -%}
{% if cookiecutter.project_type == 'cli' -%}
::: {{package_name}}.cli
{% elif cookiecutter.project_type == 'notebooks' -%}
::: {{package_name}}.utils
{% else -%}
::: {{package_name}}.example
{% endif -%}
