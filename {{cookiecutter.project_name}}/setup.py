{% set package_name = cookiecutter.project_name|lower|replace('-', '_') -%}
from setuptools import find_packages, setup

setup(
    name="{{ package_name }}",
    packages=find_packages(),
)
