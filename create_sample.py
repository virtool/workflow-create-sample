import os
import shutil

from virtool_workflow import startup, step, cleanup, fixture


@startup
async def check_db():
    pass


@step
async def make_sample_dir():
    pass


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

