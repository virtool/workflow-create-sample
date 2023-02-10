from pathlib import Path
from types import SimpleNamespace
from typing import Dict

from pyfixtures import fixture


@fixture
def intermediate() -> SimpleNamespace:
    return SimpleNamespace()


@fixture
def read_files(input_files: Dict[str, Path]):
    return [
        file.rename(f"reads_{n}.fq.gz") for file, n in zip(input_files.values(), (1, 2))
    ]
