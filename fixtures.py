from virtool_workflow_runtime.db import VirtoolDatabase
from virtool_workflow_runtime.config.configuration import db_name, db_connection_string
from virtool_workflow import fixture


@fixture
def db():
    return VirtoolDatabase(db_name(), db_connection_string)