from virtool_workflow import fixture
from virtool_workflow_runtime.config.configuration import db_name, db_connection_string
from virtool_workflow_runtime.db import VirtoolDatabase


@fixture
def db():
    return VirtoolDatabase(db_name(), db_connection_string())


@fixture
def sample_id(job_document):
    return job_document["sample_id"]


@fixture
def sample_path(data_path, sample_id):
    return data_path / f"samples/{sample_id}"


@fixture
async def document(db, sample_id):
    return await db.samples.find_one(sample_id)


@fixture
def params(job_args, temp_path, sample_id, document):
    params = dict(job_args)

    temp_sample_path = temp_path / params["sample_id"]

    params.update({
        "sample_id": sample_id,
        "sample_path": sample_path,
        "document": document,
        "files": document["files"],
        "paired": document["paired"],
        "temp_sample_path": temp_sample_path,
        "fastqc_path": temp_sample_path / "fastqc"
    })

    return params
