import shutil

import virtool_core.samples.utils
import virtool_core.utils


async def get_sample_params(params, db, sample_id, sample_path):
    document = await db.samples.find_one(sample_id)

    params.update({
        "sample_path": sample_path,
        "document": document,
        "files": document["files"],
        "paired": document["paired"]
    })


def copy_files_to_sample(paths, sample_path, proc):
    sizes = list()

    for index, path in enumerate(paths):
        suffix = index + 1
        target = virtool_core.samples.utils.join_read_path(sample_path, suffix)

        copy_or_compress(path, target, proc)

        stats = virtool_core.utils.file_stats(target)

        sizes.append(stats["size"])

    return sizes


def copy_or_compress(path, target, proc):
    if virtool_core.utils.is_gzipped(path):
        shutil.copyfile(path, target)
    else:
        virtool_core.utils.compress_file(path, target, proc)
