import os

import pytest
from virtool_workflow.fixtures.scope import WorkflowFixtureScope

import workflow


@pytest.fixture
async def mock_job(tmpdir, loop, dbi, test_db_connection_string, test_db_name):
    tmpdir.mkdir("samples")
    tmpdir.mkdir("logs").mkdir("jobs")

    job = {
        "data_path": str(tmpdir),
        "db_connection_string": test_db_connection_string,
        "db_name": test_db_name,
        "proc": 1,
        "mem": 4,
        "id": "foobar",
        "db": dbi,
    }

    await dbi.jobs.insert_one({
        "_id": "foobar",
        "task": "create_sample",
        "args": {
            "sample_id": "baz",
            "files": [
                {
                    "id": "foo.fq.gz"
                }
            ]
        }
    })

    await dbi.samples.insert_one({
        "_id": "baz",
        "paired": False,
        "files": [{
            "id": "foo.fq.gz",
            "size": 123456
        }]
    })

    document = await dbi.samples.find_one(job["id"])

    job["task_name"] = document["task"]
    job["params"] = dict(document["args"])

    job["params"].update({
        "sample_id": "baz",
        "sample_path": job["data_path"] / "samples" / "baz",
        "document": document,
        "files": document["files"],
        "paired": document["paired"]
    })

    return job


async def test_check_db(mock_job, tmpdir):
    with WorkflowFixtureScope() as scope:
        scope["params"] = mock_job["params"]
        scope["temp_path"] = tmpdir / "temp_path"

        bound_function = await scope.bind(workflow.check_db)
        bound_function()

        data_path = mock_job["data_path"]
        temp_sample_path = tmpdir / "temp_path" / "baz"

        assert mock_job["params"] == {
            "document": {
                "_id": "baz",
                "paired": False,
                "files": [{
                    "id": "foo.fq.gz",
                    "size": 123456
                }]
            },
            "fastqc_path": temp_sample_path / "fastqc",
            "files": [{
                "id": "foo.fq.gz",
                "size": 123456
            }],
            "paired": False,
            "sample_id": "baz",
            "sample_path": data_path / "samples" / "baz",
            "temp_sample_path": temp_sample_path

        }


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
