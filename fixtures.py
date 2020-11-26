from virtool_workflow import fixture
from virtool_workflow_runtime.config.configuration import db_name, db_connection_string
from virtool_workflow_runtime.db import VirtoolDatabase


@fixture
def db():
    return VirtoolDatabase(db_name(), db_connection_string)


@fixture
def sample_id(job_document):
    return job_document["sample_id"]


@fixture
def sample_path(data_path, sample_id):
    return data_path / f"samples/{sample_id}"


@fixture
def get_params(db, sample_id):
    return await db.samples.find_one(sample_id)


@fixture
def params(job_args, get_params, sample_path, sample_id):
    params = dict(job_args)

    params.update({
        "sample_id": sample_id,
        "sample_path": sample_path,
        "document": get_params,
        "files": get_params["files"],
        "paired": get_params["paired"]
    })

    return params
