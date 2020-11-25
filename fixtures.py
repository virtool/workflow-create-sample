from virtool_workflow import fixture
from virtool_workflow_runtime.config.configuration import db_name, db_connection_string
from virtool_workflow_runtime.db import VirtoolDatabase


@fixture
def db():
    return VirtoolDatabase(db_name(), db_connection_string)


@fixture
def params(job_args):
    return job_args


@fixture
def sample_id(job_document):
    return job_document["sample_id"]


@fixture
def sample_path(data_path, sample_id):
    return data_path / f"samples/{sample_id}"
