"""Shared test helpers for executing the repository's script modules.

The modules in this repository are top-level scripts (they run their logic at
import time via `print` statements) rather than importable function libraries.
To exercise them in unit tests we execute each script in an isolated namespace
and capture its stdout, then assert on the produced output / computed values.
"""

import io
import runpy
import os
from contextlib import redirect_stdout

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_script(script_name):
    """Execute ``script_name`` (relative to the repo root) as ``__main__``.

    Returns the captured stdout as a string. Any exception raised by the
    script propagates to the caller so tests can detect runtime failures.
    """
    path = os.path.join(REPO_ROOT, script_name)
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        runpy.run_path(path, run_name="__main__")
    return buffer.getvalue()
