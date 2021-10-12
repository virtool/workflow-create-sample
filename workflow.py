from pathlib import Path
from types import SimpleNamespace
from typing import Dict

from fixtures import fixture
from virtool_workflow import hooks, step
from virtool_workflow.api.samples import SampleProvider


@fixture
def intermediate():
    return SimpleNamespace()


@fixture
def read_files(input_files: Dict[str, Path]):
    return [
        file.rename(f"reads_{n}.fq.gz")
        for file, n in zip(input_files.values(), (1, 2))
    ]


@step
async def run_fastqc(
    fastqc,
    intermediate,
    read_files,
):
    """Run `fastqc` on the read files. Parse the output into a dictionary and add it to the scope."""
    intermediate.quality = await fastqc(read_files)

    return "Fastqc run completed."


@step
async def upload_read_files(sample_provider, read_files):
    """Upload the read files."""
    for file in read_files:
        await sample_provider.upload(file)


@step
async def upload_quality(sample_provider: SampleProvider, intermediate):
    """Upload the resulting quality to the sample record."""
    await sample_provider.finalize(intermediate.quality)


@hooks.on_failure
async def delete_sample(sample_provider: SampleProvider):
    """Delete the sample in the case of a failure."""
    await sample_provider.delete()
