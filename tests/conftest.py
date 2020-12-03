import motor.motor_asyncio
import pytest

from virtool_workflow_runtime.config.configuration import db_connection_string
from virtool_workflow_runtime.db import VirtoolDatabase


@pytest.fixture
def test_db_connection_string(request):
    return db_connection_string


@pytest.fixture
def test_db_name(worker_id):
    return "vt-test-{}".format(worker_id)


@pytest.fixture
def dbi(worker_id, test_db_name):
    return VirtoolDatabase(test_db_name, db_connection_string())
