#!/usr/bin/env python3
"""news-image-20261119 entrypoint.

Writes the pre-rendered front-page image (entry.png, drawn by
draw_news.py with Pillow) to the grader's output directory as entry.png.

Standard library only: the grading sandbox has no network and no
third-party packages, so this file imports nothing beyond the stdlib.
Deterministic: the same input bytes are written on every run, so both
grader runs produce identical files.
"""

import hashlib
import os
import shutil
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_IMAGE_BYTES = 1_048_576
SOURCE_FILE = "entry.png"
TARGET_FILE = "entry.png"


def fail(message):
    """Print an error to stderr and exit non-zero."""
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_source():
    """Read and validate the bundled image, returning its bytes."""
    here = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(here, SOURCE_FILE)
    if not os.path.isfile(source_path):
        fail(f"missing {SOURCE_FILE} next to {__file__}")
    with open(source_path, "rb") as handle:
        data = handle.read()
    if len(data) > MAX_IMAGE_BYTES:
        fail(f"{SOURCE_FILE} is {len(data)} bytes, over the 1 MiB limit")
    if not data.startswith(PNG_SIGNATURE):
        fail(f"{SOURCE_FILE} does not start with the PNG magic bytes")
    return data


def write_output(data):
    """Copy the bytes to the output directory and verify the copy."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target_path = os.path.join(out_dir, TARGET_FILE)
    with open(target_path, "wb") as handle:
        handle.write(data)
    digest_source = hashlib.sha256(data).hexdigest()
    with open(target_path, "rb") as handle:
        digest_target = hashlib.sha256(handle.read()).hexdigest()
    if digest_source != digest_target:
        fail("copied file does not match the source image")
    return target_path, len(data)


def main():
    data = read_source()
    target_path, size = write_output(data)
    print(f"wrote {target_path} ({size} bytes)")


if __name__ == "__main__":
    main()
