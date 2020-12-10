import os

import pytest


@pytest.mark.parametrize("exists", [None, "sample", "fastqc", "analysis"])
def test_make_sample_dir(exists, tmpdir):
    sample_path = tmpdir / "foo"

    test_make_sample_dir.params = {
        "sample_path": sample_path,
        "analysis_path": sample_path / "analysis",
        "fastqc_path": sample_path / "fastqc"
    }

    if exists is not None:
        os.makedirs(test_make_sample_dir.params[f"{exists}_path"])
