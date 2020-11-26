import os

from virtool_workflow import startup, step, cleanup
from virtool_workflow.execute import run_subprocess
import virtool_core.samples.utils

import utils


@startup
async def check_db(params, temp_path):
    """
    Instantiates params fixture.

    """
    temp_sample_path = temp_path / params["sample_id"]

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
async def copy_files(params, data_path, run_in_executor, proc, db):
    """
    Copy the files from the files directory to the nascent sample directory.

    """
    files = params["files"]
    sample_id = params["sample_id"]

    paths = [data_path / "file" / file["id"] for file in files]

    sizes = await run_in_executor(
        utils.copy_files_to_sample,
        paths,
        params["temp_sample_path"],
        proc
    )

    raw = list()

    for index, file in enumerate(files):
        name = f"reads_{index + 1}.fq.gz"

        raw.append({
            "name": name,
            "download_url": f"/download/samples/{sample_id}/{name}",
            "size": sizes[index],
            "from": file,
            "raw": True
        })

    await db.samples.update_one({"_id": sample_id}, {
        "$set": {
            "files": raw
        }
    })


@step
async def fastqc(params, run_subprocess, proc):
    """
    Runs FastQC on the renamed, trimmed read files.

    """
    read_paths = virtool_core.samples.utils.join_read_path(params["temp_sample_path"], params["paired"])

    await utils.run_fastqc(
        run_subprocess,
        proc,
        read_paths,
        params["fastqc_path"]
    )


@step
async def parse_fastqc(params, run_in_executor, db):
    """
    Capture the desired data from the FastQC output. The data is added to the samples database
    in the main run() method


    """
    qc = await run_in_executor(
        utils.parse_fastqc,
        params["fastqc_path"],
        params["temp_sample_path"]
    )

    await db.samples.update_one({"_id": params["sample_id"]}, {
        "$set": {
            "quality": qc,
            "ready": True
        }
    })


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
