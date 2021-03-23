import shutil

from virtool_core.samples.utils import join_read_path
from virtool_workflow import cleanup, step

import utils
from utils import parse_fastqc


@step
async def fetch_reads(params, data_path, run_in_executor, proc, db):
    """
    Fetch the uploaded reads being used to create this sample.

    TODO: Figure out pathing.

    """
    files = params["files"]
    sample_id = params["sample_id"]

    sizes = await run_in_executor(
        utils.copy_files_to_sample,
        paths,
        params["temp_sample_path"],
        proc
    )


@step
async def fastqc(params, sample, run_in_executor, run_subprocess, proc, work_path):
    """
    Runs FastQC on reads.

    TODO: Figure out pathing and get rid of temp_sample_path.

    """
    fastqc_path = work_path / "fastqc"

    read_paths = join_read_path(params["temp_sample_path"], sample.paired)

    await utils.run_fastqc(
        run_subprocess,
        proc,
        read_paths,
        fastqc_path
    )

    sample.quality = await run_in_executor(
        parse_fastqc,
        params["fastqc_path"],
        params["temp_sample_path"]
    )


@step
async def upload(params, run_in_executor, sample, quality):
    """
    Upload sample reads and artifacts and finalize the database record

    TODO: Figure out pathing and uploading. This is not functional here.
    TODO: Make sure file size is calculate in virtool-workflow

    """
    await sample.upload_reads(
        shutil.copytree,
        params["temp_sample_path"],
        params["sample_path"]
    )

    await sample.finalize()


@cleanup
async def delete_sample(sample):
    """
    Delete the unfinalized sample. On the server, this will trigger:
    - removal of read upload reservations
    - deletion of any sample files uploaded to server
    - removal of sample database records

    """
    await sample.delete()
