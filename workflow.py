import asyncio
from pathlib import Path
from types import SimpleNamespace

from pyfixtures import fixture
from virtool.quality.fastqc import parse_fastqc
from virtool.workflow import hooks, step, RunSubprocess
from virtool.workflow.analysis import ReadPaths
from virtool.workflow.data.samples import WFNewSample


@fixture
def intermediate() -> SimpleNamespace:
    return SimpleNamespace()


@fixture
def read_paths(new_sample: WFNewSample) -> ReadPaths:
    if len(new_sample.uploads) == 1:
        return (new_sample.uploads[0].path,)

    return new_sample.uploads[0].path, new_sample.uploads[1].path


@step(name="Run FastQC")
async def run_fastqc(
    intermediate: SimpleNamespace,
    read_paths: ReadPaths,
    run_subprocess: RunSubprocess,
    work_path: Path,
):
    """
    Run `fastqc` on the read files.

    Parse the output into a dictionary and add it to the scope.
    """
    command = [
        "fastqc",
        "-f",
        "fastq",
        "-o",
        str(work_path),
        "--extract",
        *[str(path) for path in read_paths],
    ]

    await run_subprocess(command)

    intermediate.quality = await asyncio.to_thread(parse_fastqc, work_path)



@step
async def finalize(
    intermediate: SimpleNamespace, new_sample: WFNewSample, read_paths: ReadPaths
):
    """
    Save the sample data in Virtool.

    * Upload the read files to the sample file endpoints.
    * POST the JSON quality data to sample endpoint.
    """
    for i, path in enumerate(read_paths):
        new_path = await asyncio.to_thread(path.rename, f"reads_{i + 1}.fq.gz")
        await new_sample.upload(new_path)

    await new_sample.finalize(intermediate.quality.dict())


@hooks.on_failure
async def delete_sample(new_sample: WFNewSample):
    """Delete the sample in the case of a failure."""
    await new_sample.delete()
