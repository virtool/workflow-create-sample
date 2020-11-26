import os
import shutil

from virtool_workflow import startup, step, cleanup
from utils import get_sample_params


@startup
async def check_db(params, temp_path, sample_id):
    get_sample_params()

    temp_sample_path = temp_path / sample_id

    params.update({
        "temp_sample_path": temp_sample_path,
        "fastqc_path": temp_sample_path / "fastqc"
    })


@step
async def make_sample_dir(params, run_in_executor):
    """
    Make a data directory for the sample and a subdirectory for analyses. Read files, quality data from FastQC, and
    analysis data will be stored here.

    """
    analysis_path = params["temp_sample_path"] / "analysis"

    await run_in_executor(os.makedirs, analysis_path)
    await run_in_executor(os.makedirs, params["fastqc_path"])


@step
async def copy_files():
    pass


@step
async def fastqc():
    pass


@step
async def parse_fastqc():
    pass


@step
async def upload():
    pass


@step
async def clean_watch():
    pass


@cleanup
async def delete_sample():
    pass


@cleanup
async def release_files():
    pass
