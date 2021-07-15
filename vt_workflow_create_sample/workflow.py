from types import SimpleNamespace
from typing import Dict, Path

from virtool_core.data_model import Sample
from virtool_workflow import fixture, FixtureScope, step, hooks
from virtool_workflow.api.samples import SampleProvider

__package__ = "vt_workflow_create_sample"


@fixture
def intermediate():
    return SimpleNamespace()


@step
async def download_raw_files(
    sample_provider: SampleProvider,
    input_files: Dict[str, Path],
    scope: FixtureScope,
):
    """
    Download the read files which were uploaded by the user and
    set the `sample.path` accordingly.
    """
    left = input_files.get("reads_1.fq.gz")

    sample = await sample_provider.get()

    # Set the sample path to be the download path
    sample.path = left.parent

    scope["sample"] = sample

    return "Raw reads for sample {sample.id} collected."


@step
async def upload_read_files(sample: Sample, sample_provider: SampleProvider):
    """Upload the read files."""
    await sample_provider.upload(sample.left)
    if sample.paired:
        await sample_provider.upload(sample.right)



@step
async def run_fastqc(
    fastqc,
    sample: Sample,
    scope: FixtureScope,
):
    """
    Run `fastqc` on the read files. Parse the output
    into a dictionary and add it to the scope.
    """
    read_paths = [sample.left]
    if sample.paired:
        read_paths.append(sample.right)

    scope["quality"] = await fastqc(read_paths)

    return "Fastqc run completed."


@step
async def upload_quality(sample_provider: SampleProvider, quality: dict):
    """
    Upload the resulting quality to the sample record.
    """
    await sample_provider.finalize(quality)



@hooks.on_failure
async def delete_sample(sample_provider: SampleProvider):
    """
    Delete the sample in the case of a failure.

    :param sample_provider: [description]
    :type sample_provider: SampleProvider
    """
    await sample_provider.delete()





