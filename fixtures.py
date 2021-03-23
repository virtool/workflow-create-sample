from virtool_workflow import fixture


@fixture
def quality():
    return dict()


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
