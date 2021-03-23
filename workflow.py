import os
import shutil

from virtool_workflow import startup, step, cleanup
import virtool_core.samples.utils

import utils
from utils import parse_fastqc


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
async def fastqc(params, sample, run_in_executor, run_subprocess, proc, work_path):
    """
    Runs FastQC on reads.

    """
    fastqc_path = work_path / "fastqc"

    read_paths = join_read_path(params["temp_sample_path"], sample.paired)

    await utils.run_fastqc(
        run_subprocess,
        proc,
        read_paths,
        params["fastqc_path"]
    )

    qc = await run_in_executor(
        parse_fastqc,
        params["fastqc_path"],
        params["temp_sample_path"]
    )




@step
async def upload(params, run_in_executor):
    await run_in_executor(
        shutil.copytree,
        params["temp_sample_path"],
        params["sample_path"]
    )


@step
async def clean_watch(params, db):
    """Remove the original read files from the files directory"""
    file_ids = [f["id"] for f in params["files"]]
    await db.files.delete_many({"_id": {"$in": file_ids}})


@cleanup
async def delete_sample(params, db, run_in_executor):
    await db.samples.delete_one({"_id": params["sample_id"]})

    try:
        await run_in_executor(shutil.rmtree, params["sample_path"])
    except FileNotFoundError:
        pass


@cleanup
async def release_files(params, db):
    for file_id in params["files"]:
        await db.files.update_many({"_id": file_id}, {
            "$set": {
                "reserved": False
            }
        })
