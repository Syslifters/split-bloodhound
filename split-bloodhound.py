import json
import os
from pathlib import Path

import click
import ijson


def write_chunk(filename, chunk_data, meta):
    meta["count"] = len(chunk_data)
    with open(
        filename,
        "w",
    ) as f:
        json.dump(
            {
                "data": chunk_data,
                "meta": meta,
            },
            f,
        )


@click.command()
@click.option("--input", "-i", required=True, help="Input file")
@click.option("--output-dir", "-o", help="Output directory")
@click.option("--chunksize", "-s", help="Chunk size of output files in GB")
def run(input, output_dir, chunksize):
    output_file_prefix = os.path.basename(input).rsplit(".", 1)[0]
    if not output_dir:
        output_dir = "output"
    # Create output directory if it doesn't exist
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    # Chunksize to bytes
    if not chunksize:
        chunksize = os.path.getsize(input) / 10
    chunksize = int(chunksize) * 1024 * 1024 * 1024

    file_counter = 0
    counter = 0

    with open(input, "rb") as f:
        # Get version
        meta = {k: v for k, v in ijson.kvitems(f, "meta")}
        chunk_data = []
        current_chunksize = 0
        for record in ijson.items(f, "data.item"):
            counter += 1
            record_size = len(json.dumps(record))
            if current_chunksize + record_size > chunksize:
                file_counter += 1
                filename = f"{output_dir / output_file_prefix}_{file_counter}.json"
                write_chunk(filename, chunk_data, meta)
                print(
                    f"Wrote {filename} with {len(chunk_data)} records and {current_chunksize / 1024 / 1024} MB."
                )
                chunk_data = []
            chunk_data.append(record)
            current_chunksize += record_size

        # Last chunk
        file_counter += 1
        filename = f"{output_dir / output_file_prefix}_{file_counter}.json"
        write_chunk(filename, chunk_data, meta)


if __name__ == "__main__":
    run()
