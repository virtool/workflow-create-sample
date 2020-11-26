async def get_sample_params(params, db, sample_id, sample_path):
    document = await db.samples.find_one(sample_id)

    params.update({
        "sample_path": sample_path,
        "document": document,
        "files": document["files"],
        "paired": document["paired"]
    })
