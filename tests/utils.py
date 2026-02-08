from __future__ import annotations

import os
from contextlib import contextmanager


@contextmanager
def run_within_dir(path: str):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


def file_contains_text(file: str, text: str) -> bool:
    with open(file) as f:
        return f.read().find(text) != -1
